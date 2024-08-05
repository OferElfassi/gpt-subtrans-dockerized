# GPT-SubTrans Dockerized

This repository extends and dockerizes the publicly available repository [gpt-subtrans](https://github.com/machinewrapped/gpt-subtrans). It exposes the command line interface and uses OpenAI as the AI provider. Additionally, it adds functionality to recursively translate all `.srt` files under a specified folder and its subfolders.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)
- [Meta File Structure](#meta-file-structure)
- [Credits](#credits)
- [License](#license)

## Installation

### Prerequisites

- Docker installed on your system
- OpenAI API key

### Build Docker Image

1. Build the Docker image builder stage:

    ```bash
    docker build -t gpt-subtrans-dockerized .
    ```

2. Build the Docker image runtime stage:

    ```bash
    docker build --target builder -t gpt-subtrans-dockerized .
    ```

## Usage

### Single File Translation

Run the following command to translate a single subtitle file:

```bash
docker run --rm -v [path to subtitles folder]:/app/subtitles gpt-subtrans /app/subtitles/[subtitle file] [args]
```

### Recursive Folder Translation

Run the following command to translate all `.srt` files in a folder and its subfolders:

```bash
docker run --rm -v [path to subtitles folder]:/app/subtitles gpt-subtrans /app/subtitles [args]
```

### Multi-threading Support

The `folder-subtrans.py` script supports multi-threading. Use the `--max_workers` optional argument to specify the number of concurrent files to process:

```bash
docker run --rm -v [path to subtitles folder]:/app/subtitles gpt-subtrans /app/subtitles --max_workers [number of threads] [args]
```

### Essential Arguments

- `--moviename "movie name"`
- `--description "movie description"`
- `-l [language code]`

All arguments and environment variables from the original repository can be used.

## Environment Variables

Create a `.env` file with the following variables:

```env
PROVIDER=OpenAI
OPENAI_MODEL=gpt-4o-mini
OPENAI_API_KEY=<your_openai_api_key>
MAX_BATCH_SIZE=120
# additional arguments from the original repo
```

## Meta File Structure

When translating multiple `.srt` files using the folder translate option, an optional `meta.json` file can be added in each folder containing `.srt` files or only at the top folder. The `folder-subtrans.py` script will search for metadata in the `meta.json` file starting from the current directory and traversing up to the root directory. If the `meta.json` file is not found in the current directory, it will search in the parent directory until it reaches the root directory. If the `meta.json` file is not found in any of the directories, it will use the default metadata values, which are the filename as the moviename without the extension and no description.

The file should have the following structure:

```json
{
    "file1.srt": {
        "filename": "file1.srt",
        "subtrans_args": {
            "moviename": "name"
        }
    },
    "file2.srt": {
        "filename": "file2.srt",
        "subtrans_args": {
            "moviename": "name",
            "description": "short info"
        }
    }
}
```

The script will translate each `.srt` file using the arguments passed in the `RUN` call and the ones in the `meta.json` for each `.srt` file. If the `meta.json` file does not exist when using the folder translate option, the filename without its extension will be used as the `moviename` argument.

## Credits

This repository extends the functionality of the [gpt-subtrans](https://github.com/machinewrapped/gpt-subtrans) project. Special thanks to the original authors for their work.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
