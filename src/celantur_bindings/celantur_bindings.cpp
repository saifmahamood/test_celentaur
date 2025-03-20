#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <opencv2/opencv.hpp>
#include "CelanturDetection.h"
#include "CelanturSDKInterface.h"
#include "CommonParameters.h"
#include <boost/dll.hpp>
#include <filesystem>
#include <vector>
#include <sstream>
#include <stdexcept>

namespace py = pybind11;
namespace fs = std::filesystem;

class CelanturProcessor {
public:
    // Constructor: create a processor using the license file.
    CelanturProcessor(const std::string& license_path) {
        celantur::ProcessorParams params;
        params.swapRB = true; // OpenCV loads images in BGR, SDK expects RGB.
        params.inference_plugin = "/usr/local/lib/libONNXInference.so";
        fs::path license_file(license_path);
        processor = new CelanturSDK::Processor(params, license_file);
    }

    ~CelanturProcessor() {
        delete processor;
    }

    // Load the inference model from the given path.
    void load_inference_model(const std::string& model_path) {
        fs::path model_file(model_path);
        processor->load_inference_model(model_file);
    }

    // Process the image provided as Python bytes.
    void process_image(py::bytes image_data) {
        std::string input_str = image_data;
        std::vector<uchar> buffer(input_str.begin(), input_str.end());
        cv::Mat input_img = cv::imdecode(buffer, cv::IMREAD_COLOR);
        if (input_img.empty()) {
            throw std::runtime_error("Failed to decode input image.");
        }
        processor->process(input_img);
    }

    // Get the processed image as JPEG-encoded Python bytes.
    py::bytes get_result() {
        cv::Mat result = processor->get_result();
        std::vector<uchar> out_buffer;
        if (!cv::imencode(".jpg", result, out_buffer)) {
            throw std::runtime_error("Failed to encode result image.");
        }
        std::string out_str(out_buffer.begin(), out_buffer.end());
        return py::bytes(out_str);
    }

    // Retrieve detections (to free memory).
    void get_detections() {
        processor->get_detections();
    }

    // New method: Process image and return a tuple: (JPEG result, metadata JSON)
    std::tuple<py::bytes, py::str> process_and_get_result_and_metadata(py::bytes image_data) {
        // Process the image
        std::string input_str = image_data;
        std::vector<uchar> buffer(input_str.begin(), input_str.end());
        cv::Mat input_img = cv::imdecode(buffer, cv::IMREAD_COLOR);
        if (input_img.empty()) {
            throw std::runtime_error("Failed to decode input image.");
        }
        processor->process(input_img);

        // Get the processed image (only once)
        cv::Mat out = processor->get_result();
        std::vector<uchar> out_buffer;
        if (!cv::imencode(".jpg", out, out_buffer)) {
            throw std::runtime_error("Failed to encode result image.");
        }
        std::string out_str(out_buffer.begin(), out_buffer.end());
        py::bytes result_bytes(out_str);

        // Get detections
        std::vector<celantur::CelanturDetection> dets = processor->get_detections();
        
        // Serialize detections and metrics to JSON.
        // We assume that the function serialise_image_metrics_to_json exists and takes:
        // (cv::Mat image, vector<celantur::CelanturDetection> dets, const std::string& image_name, const std::string& folder, std::ostream& out)
        // Adjust the parameters ("input_image_name", "input_folder") as needed.
        std::ostringstream oss;
        serialise_image_metrics_to_json(out, dets, "input_image_name", "input_folder", oss);
        py::str metadata_json(oss.str());

        return std::make_tuple(result_bytes, metadata_json);
    }

private:
    CelanturSDK::Processor* processor;
};

PYBIND11_MODULE(celantur_bindings, m) {
    m.doc() = "Python bindings for Celantur SDK anonymization functions";
    py::class_<CelanturProcessor>(m, "CelanturProcessor")
        .def(py::init<const std::string&>(),
             py::arg("license_path"),
             "Initialize the CelanturProcessor with the given license file path.")
        .def("load_inference_model", &CelanturProcessor::load_inference_model,
             py::arg("model_path"),
             "Load the inference model from the given model file path.")
        .def("process_image", &CelanturProcessor::process_image,
             py::arg("image_data"),
             "Process an image provided as bytes using the Celantur SDK.")
        .def("get_result", &CelanturProcessor::get_result,
             "Get the processed image as JPEG-encoded bytes.")
        .def("get_detections", &CelanturProcessor::get_detections,
             "Call get_detections to free internal memory.")
        .def("process_and_get_result_and_metadata", &CelanturProcessor::process_and_get_result_and_metadata,
             py::arg("image_data"),
             "Process the image and return a tuple of (JPEG result, metadata JSON).");
}

