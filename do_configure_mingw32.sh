# usage:
# sh /usr/bin/set-gcc-default-3.sh
# sh do_configure_mingw32.sh
# autoconf
# make
# cd lib
# make
export CXX='g++ -mno-cygwin'
export CC='gcc -mno-cygwin'
./configure --with-hts-engine-header-path=/cygdrive/c/work/github/htsengineapi/include \
  --with-hts-engine-library-path=/cygdrive/c/work/github/htsengineapi/lib \
  --build=i686-pc-mingw32 --with-charset=shift_jis 
