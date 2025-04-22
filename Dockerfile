FROM ubuntu:22.04

# Install build dependencies

RUN apt-get update && apt-get install -y \
python3 \
python3-gi \
libwnck-3-0 \
python3-psutil \
python3-cairo \
python3-distro \
i3lock \
build-essential \
libpam0g-dev \
libcairo2-dev \
libfontconfig1-dev \
libxcb-composite0-dev \
libev-dev \
libx11-xcb-dev \
libx11-dev \
libxcb1-dev \
libxcb-xkb-dev \
libxcb-xinerama0-dev \
libxcb-randr0-dev \
libxcb-image0-dev \
libxcb-util0-dev \
libxcb-xrm-dev \
libxkbcommon-dev \
libxkbcommon-x11-dev \
libjpeg-dev \
libgif-dev \
git \
autoconf \
automake \
pkg-config \
&& rm -rf /var/lib/apt/lists/\*

# Build and install i3lock-color from source

RUN git clone https://github.com/Raymo111/i3lock-color.git /tmp/i3lock-color \
&& cd /tmp/i3lock-color \
&& autoreconf -fiv \
&& ./configure --prefix=/usr --sysconfdir=/etc \
&& make \
&& make install \
&& mv /usr/bin/i3lock /usr/bin/i3lock-color \
&& rm -rf /tmp/i3lock-color

# Create directories for installation

RUN mkdir -p /usr/share/i3-logout /usr/bin /etc

# Copy the i3-logout files into the container

COPY i3-logout /usr/share/i3-logout

# Copy the installation script

COPY install-i3-logout.sh /install-i3-logout.sh

# Run the installation script

RUN chmod +x /install-i3-logout.sh && /install-i3-logout.sh

# Test the installation by checking if the binary exists

CMD ["sh", "-c", "if command -v i3-logout >/dev/null; then echo 'i3-logout is installed'; else echo 'i3-logout installation failed'; exit 1; fi"]
