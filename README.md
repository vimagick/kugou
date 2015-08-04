kugou
=====

## Up and Running

docker-compose.yml

```
kugou:
  image: vimagick/kugou
  ports:
    - "7590:80"
  restart: always
```

## RESTful API

search

```
$ http 7590:/search/lucky\ twice
```

resolve

```
$ http 7590:/resolve/13DB6FDC5B0B7FFB62555F7C8A6CCE1F
```

lyric

```
$ http 7590:/lyric/13DB6FDC5B0B7FFB62555F7C8A6CCE1F
```
