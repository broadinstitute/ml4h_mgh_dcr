# Use the official miniconda image as the base image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file to the container
COPY environment.yml .

# Create the conda environment from the environment.yml file
RUN conda env create -f environment.yml

# Activate the environment and ensure it works in future Docker commands
# Add the conda environment to the default environment path
RUN echo "source activate $(head -n 1 environment.yml | cut -d ' ' -f 2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -n 1 environment.yml | cut -d ' ' -f 2)/bin:$PATH

# Copy the folder from the host to the container
COPY ingest_parquet.py /app/

# Specify the command to run within the container
# CMD ["bash"]

