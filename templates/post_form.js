function http_post(url, params) {
            var temp = document.createElement("from");
            temp.action = url;
            temp.method = "post";
            temp.style.display = 'none';

            for (var x in params) {
                var opt = document.createElement('textarea');
                opt.name = x;
                opt.value = params[x];
                temp.appendChild(opt);
            }
            document.body.appendChild(temp)
            temp.submit();
            return temp
        }

        var params = {
            "spider": "VirusSpider",
            "city": "廊坊"
        }
        http_post('http://49.232.84.13:80/virus', params = params)