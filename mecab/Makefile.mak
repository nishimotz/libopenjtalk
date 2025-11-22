
all:
	cd src
	nmake /f Makefile.mak
	cd ..
	if exist src\libmecab.dll copy /Y src\libmecab.dll ..\..\libmecab.dll

clean:
	cd src
	nmake /f Makefile.mak clean
	cd ..
