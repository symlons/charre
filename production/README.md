kubectl create secret docker-registry gitlabregcred \
  --docker-server=registry.gitlab.com \
  --docker-username=user_name \
  --docker-password=password \
  --namespace=losstracker

