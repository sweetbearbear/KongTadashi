let obj = JSON.parse($response.body);
obj.ads = []; // 清空广告列表
obj.data = []; // 清空广告数据
obj.list = []; // 防止广告再生效
$done({ body: JSON.stringify(obj) });