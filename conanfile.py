from conans import ConanFile, CMake, tools
import os, platform

glfw_version = os.getenv('GLFW_VERSION', '0.0')
glfw_commit = os.getenv('GLFW_COMMIT', '')

class GLFWConan(ConanFile):
    name = "glfw"
    license = "MIT"
    url = "https://github.com/BentouDev/conan-glfw"
    version = glfw_version
    commit = glfw_commit

    description = "GLFW is an Open Source, multi-platform library for OpenGL, OpenGL ES and Vulkan development on the desktop."
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    exports_sources = ["glfw-source/*"]

    options = {"build_type": ["Release", "Debug", "RelWithDebInfo", "MinSizeRel"]}
    default_options = "build_type=MinSizeRel",

    def package_id(self):
        self.info.include_build_settings()
        self.info.settings.compiler
        self.info.settings.arch
        self.info.settings.build_type

    def build(self):
        # Workaround for conan choosing cmake embedded in Visual Studio
        if platform.system() == "Windows" and 'AZURE' in os.environ:
            cmake_path = '"C:\\Program Files\\CMake\\bin\\cmake.exe"'
            print (' [DEBUG] Forcing CMake : ' + cmake_path)
            os.environ['CONAN_CMAKE_PROGRAM'] = cmake_path

        cmake = CMake(self)
        cmake.definitions["GLFW_BUILD_EXAMPLES"] = False
        cmake.definitions["GLFW_BUILD_TESTS"] = False
        cmake.definitions["GLFW_BUILD_DOCS"] = False
        cmake.configure(source_folder="glfw-source")
        cmake.build()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        self.env_info.PKG_CONFIG_PATH.append(os.path.join(self.package_folder, "lib", "pkgconfig"))
        for file in os.listdir(os.path.join(self.package_folder, "lib", "pkgconfig")):
            setattr(self.env_info, "PKG_CONFIG_%s_PREFIX" % file[:-3].replace(".", "_").replace("-", "_").upper(), self.package_folder)
        self.env_info.SOURCE_PATH.append(os.path.join(self.package_folder, "src"))
        self.cpp_info.srcdirs.append("src")
