# Use a minimal base image
FROM debian:bullseye-slim

# Set the working directory
WORKDIR /build

# Install system dependencies for OCRmyPDF
RUN apt-get update && apt-get install -y \
    wget \
    tesseract-ocr \
    tesseract-ocr-all \
    pngquant \
    libjpeg-dev \
    libpng-dev \
    autotools-dev \
    automake \
    libtool \
    libleptonica-dev \
    git \
    build-essential \
    curl \
    libtiff5-dev \
    libfontconfig1-dev \
    libicu-dev \
    libfreetype6-dev \
    libpcre3-dev \
    libopenjp2-7-dev \
    zip && \
    apt-get clean

# Clone, build, and install JBIG2 encoder
RUN git clone https://github.com/agl/jbig2enc && \
    cd jbig2enc && \
    ./autogen.sh && \
    ./configure && \
    make && \
    make install

# Download and install Ghostscript
RUN curl -L https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs9561/ghostscript-9.56.1.tar.gz -o ghostscript.tar.gz && \
    tar -xzf ghostscript.tar.gz && \
    cd ghostscript-9.56.1 && \
    ./configure && make && make install && \
    cd .. && rm -rf ghostscript-9.56.1 ghostscript.tar.gz

# Bundle system dependencies into a zip file
RUN mkdir /package && \
    cp -r /usr/local/bin /usr/local/lib /usr/local/include /usr/share/tesseract-ocr /package/ && \
    zip -r /build/dependencies.zip /package

# Output the zip file
CMD ["cp", "/build/dependencies.zip", "/output/"]
