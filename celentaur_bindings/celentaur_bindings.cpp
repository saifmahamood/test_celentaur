#include <pybind11/pybind11.h>
#include <opencv2/opencv.hpp>
#include "CelanturDetection.h"
#include "CelanturSDKInterface.h"
#include "CommonParameters.h"
#include <boost/dll.hpp>
#include <filesystem>
#include <vector>
#include <stdexcept>

namespace py = pybind11;
namespace fs = std::filesystem;

// A wrapper class around CelanturSDK::Processor to expose individual functions.
class CelanturProcessor {
public:
    // The constructor creates a new processor using the provided license file.
    // It sets up default parameters (like swapRB and inference_plugin).
    CelanturProcessor(const std::string& license_path) {
        celantur::ProcessorParams params;
        params.swapRB = true; // OpenCV loads images in BGR, SDK expects RGB.
        
        // Set the CPU inference plugin location (adjust if needed).
        params.inference_plugin = "/usr/local/lib/libONNXInference.so";
        
        // Create the processor using the license file.
        fs::path license_file(license_path);
        processor = new CelanturSDK::Processor(params, license_file);
    }

    ~CelanturProcessor() {
        delete processor;
    }

    // Loads the inference model from the given path.
    void load_inference_model(const std::string& model_path) {
        fs::path model_file(model_path);
        processor->load_inference_model(model_file);
    }

    // Processes an image provided as bytes.
    // The image is decoded using OpenCV, then processed by the SDK.
    void process_image(py::bytes image_data) {
        std::string image_str = image_data;
        std::vector<uchar> img_buffer(image_str.begin(), image_str.end());
        cv::Mat input_img = cv::imdecode(img_buffer, cv::IMREAD_COLOR);
        if (input_img.empty()) {
            throw std::runtime_error("Failed to decode input image.");
        }
        processor->process(input_img);
    }

    // Retrieves the processed image result as JPEG-encoded bytes.
    py::bytes get_result() {
        cv::Mat result = processor->get_result();
        std::vector<uchar> out_buffer;
        if (!cv::imencode(".jpg", result, out_buffer)) {
            throw std::runtime_error("Failed to encode result image.");
        }
        std::string out_str(out_buffer.begin(), out_buffer.end());
        return py::bytes(out_str);
    }

    // Retrieves detections (to free memory or for further processing).
    // Here we simply call the method with no return value.
    void get_detections() {
        processor->get_detections();
    }

private:
    CelanturSDK::Processor* processor;
};

PYBIND11_MODULE(celentaur_bindings, m) {
    m.doc() = "Python bindings for Celantaur SDK anonymization functions";

    py::class_<CelanturProcessor>(m, "CelanturProcessor")
        .def(py::init<const std::string&>(),
             py::arg("license_path"),
             "Initialize the CelanturProcessor with the given license file path.")
        .def("load_inference_model", &CelanturProcessor::load_inference_model,
             py::arg("model_path"),
             "Load the inference model from the given model file path.")
        .def("process_image", &CelanturProcessor::process_image,
             py::arg("image_data"),
             "Process an image provided as bytes using the Celantaur SDK.")
        .def("get_result", &CelanturProcessor::get_result,
             "Get the processed image as JPEG-encoded bytes.")
        .def("get_detections", &CelanturProcessor::get_detections,
             "Retrieve and free detections from the processor.");
}
