# 📊 KubeMetrics Exporter

A tool for collecting metrics from Kubernetes clusters and exposing them in Prometheus format.

## 🔍 Overview

This project collects metrics for resources (Pods, Containers, etc.) in specific Kubernetes namespaces and provides them in a format that can be scraped by Prometheus. Key metrics include CPU usage, memory usage, CPU requests, CPU limits, memory requests, memory limits, and more.

## ✨ Features

- 📋 Collection of Pod information from specific namespaces
- 📈 Monitoring of resource usage by container (CPU, memory)
- 📝 Collection of resource request and limit information
- 🔄 Provision of metrics endpoint in Prometheus format
- 🔑 Cluster access via kubeconfig or in-cluster configuration

## 🚀 Installation

### 📋 Prerequisites

- 🐍 Python 3.11 or higher
- ☸️ Access to a Kubernetes cluster

### 🔧 Install

```bash
# Create virtual environment (optional)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate  # Windows

# Install package
pip install .
```

## 📝 Usage

```bash
# Basic usage
python kubemetrics_exporter.py --namespace default --port 8000

# View help
python kubemetrics_exporter.py --help
```

### ⚙️ Parameters

- `--namespace`, `-n`: Kubernetes namespace to monitor (default: default)
- `--port`, `-p`: Port to expose Prometheus metrics on (default: 8000)

### 🌐 Access URL

Once the application is running, you can access metrics at the following address:

```
http://localhost:8000
```

Prometheus server can be configured to scrape this endpoint to collect the metrics.

## 📊 Metric List

The main metrics collected are:

- `pod_cpu_usage_cores`: CPU usage by container (in cores)
- `pod_memory_usage_bytes`: Memory usage by container (in bytes)
- `pod_cpu_request_cores`: CPU requests by container (in cores)
- `pod_cpu_limit_cores`: CPU limits by container (in cores)
- `pod_memory_request_bytes`: Memory requests by container (in bytes)
- `pod_memory_limit_bytes`: Memory limits by container (in bytes)
- `pod_info`: Pod information (node, status, creation time, etc.)

### 📋 Output Example

Here's an example of the data returned from the metrics endpoint:

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 259.0
python_gc_objects_collected_total{generation="1"} 369.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 169.0
python_gc_collections_total{generation="1"} 15.0
python_gc_collections_total{generation="2"} 1.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="11",patchlevel="11",version="3.11.11"} 1.0
# HELP pod_cpu_usage_cores CPU usage in cores
# TYPE pod_cpu_usage_cores gauge
pod_cpu_usage_cores{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.001158201
# HELP pod_memory_usage_bytes Memory usage in bytes
# TYPE pod_memory_usage_bytes gauge
pod_memory_usage_bytes{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 1.1743232e+07
# HELP pod_cpu_request_cores CPU request in cores
# TYPE pod_cpu_request_cores gauge
pod_cpu_request_cores{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.0
# HELP pod_cpu_limit_cores CPU limit in cores
# TYPE pod_cpu_limit_cores gauge
pod_cpu_limit_cores{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.0
# HELP pod_memory_request_bytes Memory request in bytes
# TYPE pod_memory_request_bytes gauge
pod_memory_request_bytes{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.0
# HELP pod_memory_limit_bytes Memory limit in bytes
# TYPE pod_memory_limit_bytes gauge
pod_memory_limit_bytes{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.0
# HELP pod_info_info Pod information
# TYPE pod_info_info gauge
pod_info_info{creation_timestamp="2025-04-03T17:31:32Z",name="nfs-subdir-external-provisioner-6475d9d87-g564t",namespace="default",node="nknode03",pod="nfs-subdir-external-provisioner-6475d9d87-g564t",status="Running"} 1.0
```

## ❓ Troubleshooting

### 🚨 Metrics API Access Errors

If you encounter errors accessing the metrics API, check the following:

1. ✅ Verify that metrics-server is installed in your cluster
2. 🧪 Test that metrics access is possible via kubectl commands
3. 🔒 Confirm that appropriate RBAC permissions are configured

## 📦 Dependencies

- ☸️ kubernetes: Kubernetes API client
- 📊 prometheus-client: Prometheus metrics creation and exposition
- 🌐 requests: HTTP request handling
- 🔄 urllib3: HTTP client

## 📄 License

This project is provided as open source.

---

# 📊 KubeMetrics Exporter

쿠버네티스 클러스터의 메트릭을 수집하여 Prometheus 형식으로 노출시키는 도구입니다.

## 🔍 개요

이 프로젝트는 특정 쿠버네티스 네임스페이스의 리소스(Pod, Container 등)에 대한 메트릭을 수집하고, 이를 Prometheus가 스크래핑할 수 있는 형태로 제공합니다. 주요 메트릭으로는 CPU 사용량, 메모리 사용량, CPU 요청량, CPU 제한량, 메모리 요청량, 메모리 제한량 등이 있습니다.

## ✨ 기능

- 📋 특정 네임스페이스의 Pod 정보 수집
- 📈 컨테이너별 리소스 사용량 모니터링 (CPU, 메모리)
- 📝 리소스 요청 및 제한 정보 수집
- 🔄 Prometheus 형식의 메트릭 엔드포인트 제공
- 🔑 kubeconfig 또는 in-cluster 설정을 통한 클러스터 접근

## 🚀 설치 방법

### 📋 필수 조건

- 🐍 Python 3.11 이상
- ☸️ Kubernetes 클러스터 접근 권한

### 🔧 설치

```bash
# 가상환경 생성 (선택사항)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows

# 패키지 설치
pip install .
```

## 📝 사용 방법

```bash
# 기본 사용법
python kubemetrics_exporter.py --namespace default --port 8000

# 도움말 보기
python kubemetrics_exporter.py --help
```

### ⚙️ 매개변수

- `--namespace`, `-n`: 모니터링할 쿠버네티스 네임스페이스 (기본값: default)
- `--port`, `-p`: Prometheus 메트릭을 노출할 포트 (기본값: 8000)

### 🌐 접속 주소

애플리케이션이 실행되면 다음 주소로 메트릭에 접근할 수 있습니다:

```
http://localhost:8000
```

Prometheus 서버에서는 이 주소를 스크래핑 대상으로 설정하여 메트릭을 수집할 수 있습니다.

## 📊 메트릭 목록

수집되는 주요 메트릭은 다음과 같습니다:

- `pod_cpu_usage_cores`: 컨테이너별 CPU 사용량 (코어 단위)
- `pod_memory_usage_bytes`: 컨테이너별 메모리 사용량 (바이트 단위)
- `pod_cpu_request_cores`: 컨테이너별 CPU 요청량 (코어 단위)
- `pod_cpu_limit_cores`: 컨테이너별 CPU 제한량 (코어 단위)
- `pod_memory_request_bytes`: 컨테이너별 메모리 요청량 (바이트 단위)
- `pod_memory_limit_bytes`: 컨테이너별 메모리 제한량 (바이트 단위)
- `pod_info`: Pod 정보 (노드, 상태, 생성 시간 등)

### 📋 출력 예시

다음은 메트릭 엔드포인트에서 반환되는 데이터의 예시입니다:

```
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 259.0
python_gc_objects_collected_total{generation="1"} 369.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable objects found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 169.0
python_gc_collections_total{generation="1"} 15.0
python_gc_collections_total{generation="2"} 1.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="11",patchlevel="11",version="3.11.11"} 1.0
# HELP pod_cpu_usage_cores CPU usage in cores
# TYPE pod_cpu_usage_cores gauge
pod_cpu_usage_cores{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.001158201
# HELP pod_memory_usage_bytes Memory usage in bytes
# TYPE pod_memory_usage_bytes gauge
pod_memory_usage_bytes{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 1.1743232e+07
# HELP pod_cpu_request_cores CPU request in cores
# TYPE pod_cpu_request_cores gauge
pod_cpu_request_cores{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.0
# HELP pod_cpu_limit_cores CPU limit in cores
# TYPE pod_cpu_limit_cores gauge
pod_cpu_limit_cores{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.0
# HELP pod_memory_request_bytes Memory request in bytes
# TYPE pod_memory_request_bytes gauge
pod_memory_request_bytes{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.0
# HELP pod_memory_limit_bytes Memory limit in bytes
# TYPE pod_memory_limit_bytes gauge
pod_memory_limit_bytes{container="nfs-subdir-external-provisioner",namespace="default",pod="nfs-subdir-external-provisioner-6475d9d87-g564t"} 0.0
# HELP pod_info_info Pod information
# TYPE pod_info_info gauge
pod_info_info{creation_timestamp="2025-04-03T17:31:32Z",name="nfs-subdir-external-provisioner-6475d9d87-g564t",namespace="default",node="nknode03",pod="nfs-subdir-external-provisioner-6475d9d87-g564t",status="Running"} 1.0
```

## ❓ 문제 해결

### 🚨 메트릭 API 접근 오류

메트릭 API 접근 시 오류가 발생하는 경우, 다음을 확인하세요:

1. ✅ 클러스터에 metrics-server가 설치되어 있는지 확인
2. 🧪 kubectl 명령어를 통해 메트릭 접근이 가능한지 테스트
3. 🔒 적절한 RBAC 권한이 설정되어 있는지 확인

## 📦 의존성 패키지

- ☸️ kubernetes: 쿠버네티스 API 클라이언트
- 📊 prometheus-client: Prometheus 메트릭 생성 및 노출
- 🌐 requests: HTTP 요청 처리
- 🔄 urllib3: HTTP 클라이언트

## 📄 라이선스

이 프로젝트는 오픈소스로 제공됩니다. 