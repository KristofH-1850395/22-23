all: bachelor bachelor-finite contact contact-finite

contact: bin
	g++ -fopenmp -lpthread -o bin/contact.exe -O3 src/main/cpMain.cpp src/systems/abstractProcess.cpp src/systems/bachelorProcess.cpp src/systems/contactProcess.cpp src/application.cpp

contact-finite: bin
	g++ -fopenmp -lpthread -o bin/contact-finite.exe -O3 src/main/cpMainFinite.cpp src/systems/abstractProcess.cpp src/systems/bachelorProcess.cpp src/systems/contactProcess.cpp src/application.cpp

bachelor: bin
	g++ -fopenmp -lpthread -o bin/bachelor.exe -O3 src/main/bpMain.cpp src/systems/abstractProcess.cpp src/systems/bachelorProcess.cpp src/systems/contactProcess.cpp src/application.cpp

bachelor-finite: bin
	g++ -fopenmp -lpthread -o bin/bachelor-finite.exe -O3 src/main/bpMainFinite.cpp src/systems/abstractProcess.cpp src/systems/bachelorProcess.cpp src/systems/contactProcess.cpp src/application.cpp

bin:
	mkdir bin 2> /dev/null || true

clean:
	rm bin/* 2> /dev/null || true
	rmdir bin 2> /dev/null || true 
