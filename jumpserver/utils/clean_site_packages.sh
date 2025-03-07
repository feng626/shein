#!/bin/bash

lib_path="/opt/py3/lib/python3.11/site-packages"

# 清理不需要的模块
need_clean="jedi"
for i in $need_clean; do
  rm -rf "${lib_path}/${i}"
done

# 清理缓存文件
cd ${lib_path} || exit 1
find . -name "*.pyc" -exec rm -f {} \;

# 清理不需要的国际化文件
find . -name 'locale' -o -name 'locales' -type d | while read -r dir; do
    find "$dir" -mindepth 1 -maxdepth 1 -type d \
      ! -name 'zh_Hans' \
      ! -name 'zh_CN' \
      ! -name 'en' \
      ! -name 'en_US' \
      ! -name 'ja' \
      ! -name 'fr' \
      -exec rm -rf {} \;
done
