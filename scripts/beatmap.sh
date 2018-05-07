docker run \
  -i -t \
  --rm \
  -u tong \
  --name beatmap \
  --volume ~/Projects/beatmap:/home/tong/beatmap \
  beatmap:sklearn

