# for cygwin gcc3
export CXX='g++ -mno-cygwin'
export CC='gcc -mno-cygwin'
sh /usr/bin/set-gcc-default-3.sh
echo 'building htsengineapi'
pushd ../../htsengineapi
  make clean
  autoconf
  ./configure --build=i686-pc-mingw32
  make
popd
echo 'building libopenjtalk'
pushd ..
  make clean
  sh do_configure_mingw32.sh
  autoconf
  make
popd
echo 'building DLL'
make -f Makefile.mingw32 clean
make -f Makefile.mingw32 clean-dll htsengineapi njd_set_unvoiced_vowel libjpcommon libopenjtalk.dll
strip libopenjtalk.dll
