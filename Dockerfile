# Use the Rust Alpine image as the base
FROM rust:1.73-alpine AS builder

# Add the musl-dev and openssl-dev packages (FUCK YOU OPENSSL)
RUN apk add musl-dev openssl-dev

# Set the current working directory in the container
WORKDIR /usr/src/eirlys_rs

# Copy the current directory contents into the container
COPY . .

# Build the application
RUN cargo build --release

# Start a new stage to create a lean final image
FROM alpine:latest

# Set the current working directory in the container
WORKDIR /usr/local/bin

# Copy the binary from the builder stage to the current stage
COPY --from=builder /usr/src/eirlys_rs/target/release/eirlys_rs .

# Expose port 3030
EXPOSE 3030

# Run the application
CMD ["./eirlys_rs"]