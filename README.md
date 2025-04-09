## Get the Project and Initialize
```
git clone https://github.com/VmLia/books-mcp-server.git
cd books-mcp-server
uv venv
```
if macbook or linux
````
source .venv/bin/activate
````
if windows
````
.venv\Scripts\activate.bat
````

### Install Python Packages
```
uv add "mcp[cli]" httpx openai beautifulsoup4 lxml 
```
If the network is slow, you can set up a domestic mirror source.
```
uv add "mcp[cli]" httpx openai beautifulsoup4 lxml --index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

## Example of Using cherry-studio
**Method 1**: On the setting page of cherry-studio, click on the MCP server, then click "Add Server", and subsequently configure it on the page.
### Type
```
STDIO
```
### Command
```
uv
```
### Parameters
```
--directory
# your project dir
run
main.py
```

**Method 2**: Use the configuration parameters
```
{
  "mcpServers": {
    "books-mcp-server": {
      "name": "books-mcp",
      "type": "stdio",
      "description": "",
      "isActive": true,
      "registryUrl": "",
      "command": "uv",
      "args": [
        "--directory",
        "/Enter your local project directory/books-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
```