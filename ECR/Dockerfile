FROM --platform=linux/x86_64 python:3.12.1-alpine3.19

ENV PYTHONIOENCODING utf-8
WORKDIR /app

RUN apk add --update \
        wget \
        # Add chromium and dependences
        udev \
        ttf-freefont \
        chromium \
        chromium-chromedriver

RUN apk add --no-cache unzip

# Add Japanese font
# Valid Download URL : https://github.com/notofonts/noto-cjk/releases/tag/Sans2.004 > Language Specific OTFs Japanese (日本語)
# Downloaded file : 06_NotoSansCJKjp.zip
RUN mkdir -p /app/noto \
    && wget -P /app/noto https://github.com/notofonts/noto-cjk/releases/download/Sans2.004/06_NotoSansCJKjp.zip \
    && unzip /app/noto/06_NotoSansCJKjp.zip -d /app/noto \
    && mkdir -p /usr/share/fonts/noto \
    && cp /app/noto/*.otf /usr/share/fonts/noto \
    && chmod 644 -R /usr/share/fonts/noto/ \
    && fc-cache -fv \
    && rm -rf /app/noto


# Add selenium
RUN pip install selenium \
    && pip install boto3 \
    && pip install undetected-chromedriver==3.5.4

COPY ./app .

CMD [ "python", "main.py" ]
