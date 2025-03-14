let url = $request.url;
let headers = $request.headers;

function notify(title = "", subtitle = "", content = "", open_url) {
    let opts = {};
    if (open_url) opts["open-url"] = open_url;
    if (Object.keys(opts).length === 0) {
        $notification.post(title, subtitle, content);
    } else {
        $notification.post(title, subtitle, content, opts);
    }
}

(async function launch() {
    if (headers["User-Agent"] && (headers["User-Agent"].includes("Blued") || headers["User-Agent"].includes("Media"))) {
        notify("🐓", "点击跳转到浏览器打开看图", url, url);
        console.log(url);
    }
    $done({});
})();
