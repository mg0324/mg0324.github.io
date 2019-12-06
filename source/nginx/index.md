---
title: nginx专页
date: 2019-08-06 18:39:27
---

* 1.nginx 的一段反向代理配置

    
        server {
            listen 80;
            server_name local.voidking.com;
            charset utf-8;
            location /{
                proxy_set_header   Host             $host;
                proxy_set_header   X-Real-IP        $remote_addr;
                proxy_set_header  X-Forwarded-For  $proxy_add_x_forwarded_for;
                client_max_body_size       1024m;
                client_body_buffer_size    128k;
                client_body_temp_path      data/client_body_temp;
                proxy_connect_timeout      90;
                proxy_send_timeout         90;
                proxy_read_timeout         90;
                proxy_buffer_size          4k;
                proxy_buffers              4 32k;
                proxy_busy_buffers_size    64k;
                proxy_temp_file_write_size 64k;
                proxy_temp_path            data/proxy_temp;
                
                proxy_pass http://127.0.0.1:8090;
            }
        }

