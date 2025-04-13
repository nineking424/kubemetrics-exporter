# KubeMetrics Exporter

쿠버네티스 클러스터의 메트릭을 수집하여 Prometheus 형식으로 노출시키는 도구입니다.

## 개요

이 프로젝트는 특정 쿠버네티스 네임스페이스의 리소스(Pod, Container 등)에 대한 메트릭을 수집하고, 이를 Prometheus가 스크래핑할 수 있는 형태로 제공합니다. 주요 메트릭으로는 CPU 사용량, 메모리 사용량, CPU 요청량, CPU 제한량, 메모리 요청량, 메모리 제한량 등이 있습니다.

## 기능

- 특정 네임스페이스의 Pod 정보 수집
- 컨테이너별 리소스 사용량 모니터링 (CPU, 메모리)
- 리소스 요청 및 제한 정보 수집
- Prometheus 형식의 메트릭 엔드포인트 제공
- kubeconfig 또는 in-cluster 설정을 통한 클러스터 접근

## 설치 방법

### 필수 조건

- Python 3.11 이상
- Kubernetes 클러스터 접근 권한

### 설치

```bash
# 가상환경 생성 (선택사항)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows

# 패키지 설치
pip install .
```

## 사용 방법

```bash
# 기본 사용법
python kubemetrics_exporter.py --namespace default --port 8000

# 도움말 보기
python kubemetrics_exporter.py --help
```

### 매개변수

- `--namespace`, `-n`: 모니터링할 쿠버네티스 네임스페이스 (기본값: default)
- `--port`, `-p`: Prometheus 메트릭을 노출할 포트 (기본값: 8000)

## 메트릭 목록

수집되는 주요 메트릭은 다음과 같습니다:

- `pod_cpu_usage_cores`: 컨테이너별 CPU 사용량 (코어 단위)
- `pod_memory_usage_bytes`: 컨테이너별 메모리 사용량 (바이트 단위)
- `pod_cpu_request_cores`: 컨테이너별 CPU 요청량 (코어 단위)
- `pod_cpu_limit_cores`: 컨테이너별 CPU 제한량 (코어 단위)
- `pod_memory_request_bytes`: 컨테이너별 메모리 요청량 (바이트 단위)
- `pod_memory_limit_bytes`: 컨테이너별 메모리 제한량 (바이트 단위)
- `pod_info`: Pod 정보 (노드, 상태, 생성 시간 등)

## 문제 해결

### 메트릭 API 접근 오류

메트릭 API 접근 시 오류가 발생하는 경우, 다음을 확인하세요:

1. 클러스터에 metrics-server가 설치되어 있는지 확인
2. kubectl 명령어를 통해 메트릭 접근이 가능한지 테스트
3. 적절한 RBAC 권한이 설정되어 있는지 확인

## 의존성 패키지

- kubernetes: 쿠버네티스 API 클라이언트
- prometheus-client: Prometheus 메트릭 생성 및 노출
- requests: HTTP 요청 처리
- urllib3: HTTP 클라이언트

## 라이선스

이 프로젝트는 오픈소스로 제공됩니다. 