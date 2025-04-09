import logging
from bs4 import BeautifulSoup
import httpx
from mcp.server import FastMCP

# 配置日志记录
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

# 初始化 FastMCP 服务器
app = FastMCP('books-mcp-server')


@app.tool()
async def book_search(query: str) -> str:
    """
    搜索图书信息

    Args:
        query: 要搜索的图书关键词

    Returns:
        搜索到的图书信息总结
    """
    service_url = f"http://www.shuchacha.net/s?wd={query}"
    headers = {}

    try:
        # 使用 httpx 发送异步 GET 请求
        async with httpx.AsyncClient() as client:
            response = await client.get(service_url, headers=headers)
        # 检查响应状态码
        response.raise_for_status()

        # 使用日志记录 response.text
        
        # 修改解析器为 html.parser
        soup = BeautifulSoup(response.text, 'lxml')

        # 查找所有图书结果的容器
        book_containers = soup.find_all('div', class_='result c-container')

        # 存储提取的图书信息
        books = []

        for container in book_containers:
            # 提取书名
            h3_tag = container.find('h3', class_='t c-title-en')
            if h3_tag:
                title_tag = h3_tag.find('a')
                if title_tag:
                    title = title_tag.text.strip()
                    # 提取书本对应的 URL
                    book_url = title_tag.get('href')
                else:
                    title = '未找到书名信息'
                    book_url = '未找到URL信息'
            else:
                title = '未找到书名信息'
                book_url = '未找到URL信息'

            # 提取作者、页数、出版社和出版日期
            info_span = container.find('span', class_='c-showurl')
            if info_span:
                author_tag = info_span.find('b', string='作者:')
                if author_tag and author_tag.next_sibling and isinstance(author_tag.next_sibling, str):
                    author = author_tag.next_sibling.strip()
                else:
                    author = '未找到作者信息'

                pages_tag = info_span.find('b', string='页数:')
                if pages_tag and pages_tag.next_sibling and isinstance(pages_tag.next_sibling, str):
                    pages = pages_tag.next_sibling.strip()
                else:
                    pages = '未找到页数信息'

                publisher_tag = info_span.find('b', string='出版社:')
                if publisher_tag and publisher_tag.next_sibling and isinstance(publisher_tag.next_sibling, str):
                    publisher = publisher_tag.next_sibling.strip()
                else:
                    publisher = '未找到出版社信息'

                publish_date_tag = info_span.find('b', string='出版日期:')
                if publish_date_tag and publish_date_tag.next_sibling and isinstance(publish_date_tag.next_sibling, str):
                    publish_date = publish_date_tag.next_sibling.strip()
                else:
                    publish_date = '未找到出版日期信息'
            else:
                author = '未找到作者信息'
                pages = '未找到页数信息'
                publisher = '未找到出版社信息'
                publish_date = '未找到出版日期信息'

            # 提取简介
            abstract_spans = container.find_all('span', class_='c-abstract')
            abstracts = []
            for span in abstract_spans:
                # 跳过主题词的 span
                if '主题词:' not in span.text:
                    abstracts.append(span.text.strip())
            if abstracts:
                # 若有多个简介段落，合并为一个字符串
                book_abstract = ' '.join(abstracts)
            else:
                book_abstract = '未找到简介信息'

            # 将提取的信息存储为字典
            book_info = {
                '书名': title,
                '作者': author,
                '页数': pages,
                '出版社': publisher,
                '出版日期': publish_date,
                'URL': "http://www.shuchacha.net" + book_url,
                '简介': book_abstract
            }
            books.append(book_info)

        # 生成搜索结果总结
        result_summary = ""
        for book in books:
            result_summary += f"书名: {book['书名']}\n"
            result_summary += f"作者: {book['作者']}\n"
            result_summary += f"页数: {book['页数']}\n"
            result_summary += f"出版社: {book['出版社']}\n"
            result_summary += f"出版日期: {book['出版日期']}\n"
            result_summary += f"URL: {book['URL']}\n"
            result_summary += f"简介: {book['简介']}\n"
            result_summary += "=" * 10 + "\n"

        return result_summary+"【请帮我整理以上书本信息，要求格式规范整齐，将书名显示成超链接点击打开URL对应的地址，对每本书的简介进行扩写介绍100字以上。】"

    except httpx.ConnectTimeout:
        logging.error("连接超时，请检查网络或服务配置。")
        return "连接超时，请检查网络或服务配置。"
    except httpx.RequestError as e:
        logging.error(f"请求发生错误: {e}")
        return f"请求发生错误: {e}"
    except Exception as e:
        logging.error(f"执行 book_search 工具时发生未知错误: {e}", exc_info=True)
        return f"执行 book_search 工具时发生未知错误: {e}"


if __name__ == "__main__":
    app.run(transport='stdio')
    