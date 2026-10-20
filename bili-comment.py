from bilibili_api import video, sync
import pandas as pd

# ========== 配置区域（本地运行时修改这里） ==========
# 【重要】真实SESSDATA只在本地填写，不要提交真实密钥到GitHub
SESSDATA = "在此粘贴B站SESSDATA，请勿上传真实账号凭证"
# B站视频BV号，例如 BV1xx411c7mZ
bv_id = "替换成目标视频BV号"
limit = 20
# ==============================================

def get_bilibili_comments(bv, sessdata):
    v = video.Video(bvid=bv, credential={"sessdata": sessdata})
    all_comments = []
    page = 1
    while True:
        try:
            reply_data = sync(v.get_comments(page=page, limit=limit))
            comments = reply_data["replies"]
            if not comments:
                break
            for c in comments:
                info = {
                    "用户名": c["member"]["uname"],
                    "评论内容": c["content"]["message"],
                    "点赞数": c["like"],
                    "发布时间": c["ctime"]
                }
                all_comments.append(info)
            page += 1
        except Exception as e:
            print("采集结束或者触发限制：", e)
            break
    return all_comments

if __name__ == "__main__":
    comment_list = get_bilibili_comments(bv_id, SESSDATA)
    df = pd.DataFrame(comment_list)
    df.to_excel("b站评论.xlsx", index=False)
    print(f"一共采集到 {len(comment_list)} 条评论，保存到 b站评论.xlsx")
