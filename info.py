import  requests
import  json
list=[]
def get_domain_info(id,token):
    url="https://dnsapi.cn/Domain.List"
    login_token=id+","+token
    payload={"login_token":login_token}
    content=requests.post(url,data=payload).text
    json_info=(json.loads(content))
    for domain in json_info["domains"]:
        print(domain["id"], domain["name"])
        get_record_id(login_token,domain["id"])
def get_record_id(login_token,domain_id):
    url = "https://dnsapi.cn/Record.List"
    payload = {"login_token": login_token,"domain_id":domain_id}
    content = requests.post(url, data=payload).text
    json_info = (json.loads(content))
    # print(json_info)
    ipgrep=r"[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}\.[0-9]\{1,3\}"
    for record in json_info["records"]:
        i=str(len(list)+1)
        print("\t"+i+"\t"+record["id"],record["type"],record["name"],record["value"],record["line_id"])
        payload="login_token={0}&format=json&domain_id={1}&record_id={2}&record_line_id={3}&sub_domain={4}".format(login_token,domain_id,record["id"],record["line_id"],record["name"])
        cmd='''
cip=$(curl -s ip.sb)
vip=$( curl -sX POST https://dnsapi.cn/Record.List -d '{0}' | grep -o '{1}' ) 
if [ $cip = $vip ]
then echo $cip
else
  curl -sX POST https://dnsapi.cn/Record.Ddns -d '{0}'
fi
'''.format(payload,ipgrep)
        list.append(cmd)
id=input("输入id：").strip()
token=input("输入token：").strip()
get_domain_info(id,token)
while(True):
    try:
        i=int(input("输入记录序号生成命令："))
        print(list[i-1])
        with open("ddns.sh","w") as f:
            f.write(list[i-1])
    except:
        print("exit")
        break