FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

# Base build tools
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    ninja-build \
    git \
    wget \
    curl \
    pkg-config \
    # OpenGL / Mesa
    libgl1-mesa-dev \
    libglu1-mesa-dev \
    mesa-utils \
    libegl1-mesa-dev \
    # GStreamer for Qt Multimedia
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libgstreamer-plugins-good1.0-dev \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good \
    gstreamer1.0-libav \
    # Audio
    libpulse-dev \
    libasound2-dev \
    # X11 / display
    libx11-dev \
    libxcb1-dev \
    libxcb-xinerama0 \
    libxcb-cursor0 \
    libxkbcommon-x11-0 \
    libxkbcommon-dev \
    # Python
    python3.10 \
    python3.10-venv \
    python3.10-dev \
    python3-pip \
    # OpenCV system deps
    libopencv-dev \
    # Misc
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Qt 6.5.0 via aqtinstall
RUN pip3 install aqtinstall && \
    aqt install-qt linux desktop 6.4.2 gcc_64 \
        --modules qtmultimedia \
        --outputdir /opt/Qt

ENV Qt6_DIR=/opt/Qt/6.4.2/gcc_64
ENV PATH=$Qt6_DIR/bin:$PATH
ENV LD_LIBRARY_PATH=$Qt6_DIR/lib:$LD_LIBRARY_PATH
ENV QML_IMPORT_PATH=$Qt6_DIR/qml
ENV QT_PLUGIN_PATH=$Qt6_DIR/plugins

# Python venv with project dependencies
RUN python3.10 -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /workspace

CMD ["/bin/bash"]
