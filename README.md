# Hbtask
## Software Development Case

Hepsiburada Task uygulaması Google Cloud üzerinde kurulmuş olan Kubernetes cluster üzerinde deploy edilmiştir.
```sh
http://35.239.122.176/
```

# TOOLS
- Python 2.7
- Flask 1.1.14

/etc/ssl/certs folderı içerisindeki pem dosyalarının up to date tarihlerini çekmektedir.

## Stepler

### 1- Create Kubernetes Cluster

Cloud Shell üzerinde aşağıdaki komutları çalıştırıyoruz

```sh
export ZONE="us-central1-c" gcloud container clusters create test-cluster --num-nodes=2 --zone=$ZONE gcloud container clusters get-credentials test-cluster --zone=$ZONE
```

### 2- Package Application

Uygulamayı localde docker yüklü bir bilgisayarda aşağıdaki komutla build edip docker.io üzerine yolluyoruz.

```sh
docker build -t erkanderon/app:v2.0.0 . 
docker push erkanderon/app:v2.0.0
```

https://hub.docker.com/repository/docker/erkanderon/app

### 3- Deploy on Kubernetes Cluster

Uygulamayı custom ns ler dışındaki yarattığımız bir ns üzerinde deploy edeceğiz. İlk olarak aşağıdaki komutla namespace create ediyoruz

```sh
kubectl apply -f namespace.yaml
```

infra folderı içerisindeki deployment-reader.yaml dosyasını Cloud Shell içerisinde aşağıdaki komutla apply ediyoruz.
```sh
kubectl apply -f deployment-reader.yaml -ns development
```


### 4- Expose App with LoadBalancer service

Ayağa kalkan uygulamayı dış dünyaya açıyoruz.

```sh
kubectl expose deployment reader-deployment --name=reader-service --type=LoadBalancer --port 80 --target-port 8000
```

### 5- Result

```sh
NAME             TYPE           CLUSTER-IP      EXTERNAL-IP      PORT(S)        AGE
kubernetes       ClusterIP      10.71.240.1     <none>           443/TCP        12d
reader-service   LoadBalancer   10.71.246.172   35.239.122.176   80:30437/TCP   74m
```
