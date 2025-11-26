## Running the C++ Test Executable

To build and run the C++ test in `tests/cpp/test_interp.cpp`:

1. Navigate to the test directory:
	```bash
	cd tests/cpp
	```
2. Create a build directory and enter it:
	```bash
	mkdir -p build
	cd build
	```
3. Run CMake to configure the project:
	```bash
	cmake ..
	```
4. Build the test executable:
	```bash
	make
	```
5. Run the test:
	```bash
	./test_interp
	```

This will compile and run the test, printing the output of the interp function.
---