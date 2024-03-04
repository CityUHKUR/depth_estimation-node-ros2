FROM ros:iron

RUN apt-get update

RUN apt-get install vim -y

COPY ./entry_point.sh /entry_point.sh

# Make the script executable
RUN chmod +x /entry_point.sh

WORKDIR /src

ENTRYPOINT [ "/entry_point.sh" ]