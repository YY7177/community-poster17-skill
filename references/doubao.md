# 豆包完整海报接入

本skill随附 `scripts/doubao_generate.py`，来源为本机doubao-image现有runner，保留其Ark协议、关闭SDK自动重试和原始响应保存方式。默认模型为已成功生成海报的 `doubao-seedream-5-0-pro-260628`，使用官方火山方舟接口；不把Nano Banana、即梦网页与Ark模型混称为同一接口。模型将来失效时报告真实错误，不自动换模型。

运行需要Python3.10+、`volcengine-python-sdk`和`httpx`。定位宿主实际可用的Python，不写死维护者盘符。先执行 `python <skill>/scripts/doubao_generate.py --check`，只返回SDK版本、模型及Key是否配置，不提交图片请求。脚本专用凭证变量为 `COMMUNITY_POSTER_ARK_API_KEY`，Windows还读取当前用户环境变量；不读取其他skill使用的 `ARK_API_KEY`。缺失时使用者在本机运行随附 `scripts/set-ark-api-key.ps1` 隐藏输入；其他平台自行在本机设置专用环境变量。88API Key与Ark Key不同，不互相代用，不将任何Key写入skill、prompt或输出文件。

## 生成与交接

```text
python <skill>/scripts/doubao_generate.py --prompt-file <本次>/prompts/poster-prompt-zh.txt --image <Nano Banana实际输出> --image <社区原图> --size 1200x1500 --output-dir <本次>/final/zh
python <skill>/scripts/doubao_generate.py --prompt-file <本次>/prompts/poster-prompt-en.txt --image <同一Nano Banana实际输出> --image <社区原图> --size 1200x1500 --output-dir <本次>/final/en
```

顺序执行，两语各一次。图1为已生成风格场景，图2为可选社区地点依据，最多10张。prompt对图的序号说明必须匹配实际传参；不用社区原图时改写第二段，不能声称上传了不存在的第二图。请求尺寸随用户规格，默认4:5的1200×1500，不在返回后再修正。当前runner默认单图、非流式、有水印；用户明确要无水印才加 `--no-watermark`。

`--dry-run`只验证请求构造且不收费；维护时可用，不要求每次逐图运行。不能把它当远程权限或成图质量证明。默认一次Nano Banana+两次豆包，共三次生成，不自动新增多版本。

## 原始返回与失败

runner识别返回图片格式、下载原始字节并保留元数据和结果链接。下载/可保存性判断不是文字、场景或质量核验。成功后直接展示全部原图，不OCR、不字形检查、不缩放转PNG、不补字、不裁切、不重新排版、不自动返修。不得在输出后声称文字或尺寸检查通过。

接口超时/断线且受理不明时停止，不自动重试。中文已成功而英文失败时先交中文和已保存prompt，如实说明英文未完成；不重发中文。只下载失败而结果URL存在时可重下既有图片，不再提交生图。新的付费请求须来自用户明确要求。记录API结果状态，不把“不核验”误当成可以伪造成功。

来源：个人 `doubao-image` skill的runner与密钥设置脚本（2026-10-12复制），没有复制凭证或个人配置。接口参考：[火山方舟图片生成API](https://docs.volcengine.com/docs/ark/image-generation-api?lang=zh)。
