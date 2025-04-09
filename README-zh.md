## 获取项目并初始化
````
git clone https://github.com/VmLia/books-mcp-server.git
cd books-mcp-server
uv venv
source .venv/bin/activate
````
如果是 macbook or linux
````
source .venv/bin/activate
````
如果是 windows
````
.venv\Scripts\activate.bat
````

### 安装python包
````
uv add "mcp[cli]" httpx openai beautifulsoup4 lxml 
````
If the network is slow, you can set up a domestic mirror source.
````
uv add "mcp[cli]" httpx openai beautifulsoup4 lxml --index-url https://pypi.tuna.tsinghua.edu.cn/simple
````

## 使用 cherry-studio 调用示例
方式一：在cherry-studio设置页面，点击MCP服务器，点击添加服务器，随后在页面中配置
### 类型
````
STDIO
````
### 命令
````
uv
````
### 参数
````
--directory
# your project dir
run
main.py
````

方式二：使用配置参数
````
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
        "/输入你本地项目目录/books-mcp-server",
        "run",
        "main.py"
      ]
    }
  }
}
````


