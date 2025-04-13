#!/usr/bin/env python3
import os
import json
import time
import argparse
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from prometheus_client import start_http_server, Gauge, Info
from prometheus_client.core import GaugeMetricFamily, InfoMetricFamily, REGISTRY
import requests
import urllib3

class KubeMetricsExporter:
    """
    KubeMetrics Exporter
    특정 네임스페이스의 모든 요소에 대한 메트릭을 수집하고 Prometheus 형식으로 변환
    """
    
    def __init__(self, namespace, metrics_port=8000):
        """
        초기화 함수
        
        Args:
            namespace (str): 모니터링할 Kubernetes 네임스페이스
            metrics_port (int): Prometheus 메트릭을 노출할 포트
        """
        self.namespace = namespace
        self.metrics_port = metrics_port
        
        # SSL 경고 무시 설정
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        
        # Kubernetes 클라이언트 설정
        try:
            # kubeconfig가 있으면 사용
            config.load_kube_config()
            print("kubeconfig를 사용하여 Kubernetes 클러스터에 연결합니다.")
        except Exception as e:
            print(f"kubeconfig 로드 실패: {str(e)}")
            try:
                # 없으면 서비스 계정 사용 (클러스터 내부에서 실행 시)
                config.load_incluster_config()
                print("in-cluster 설정을 사용하여 Kubernetes 클러스터에 연결합니다.")
            except Exception as e:
                print(f"in-cluster 설정 로드 실패: {str(e)}")
                raise Exception("Kubernetes 클러스터에 연결할 수 없습니다. kubeconfig 또는 in-cluster 설정을 확인하세요.")
            
        self.core_v1 = client.CoreV1Api()
        self.apps_v1 = client.AppsV1Api()
        
        # Prometheus 메트릭 정의
        self.pod_cpu_usage = GaugeMetricFamily(
            'pod_cpu_usage_cores',
            'CPU usage in cores',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_mem_usage = GaugeMetricFamily(
            'pod_memory_usage_bytes',
            'Memory usage in bytes',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_cpu_request = GaugeMetricFamily(
            'pod_cpu_request_cores',
            'CPU request in cores',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_cpu_limit = GaugeMetricFamily(
            'pod_cpu_limit_cores',
            'CPU limit in cores',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_mem_request = GaugeMetricFamily(
            'pod_memory_request_bytes',
            'Memory request in bytes',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_mem_limit = GaugeMetricFamily(
            'pod_memory_limit_bytes',
            'Memory limit in bytes',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_info = InfoMetricFamily(
            'pod_info',
            'Pod information',
            labels=['namespace', 'pod', 'node']
        )
    
    def collect_pod_metrics(self):
        """
        Pod 메트릭 수집
        """
        try:
            print(f"{self.namespace} 네임스페이스에서 Pod 정보 수집 중...")
            
            # 네임스페이스의 모든 Pod 목록 가져오기
            pods = self.core_v1.list_namespaced_pod(self.namespace)
            print(f"{len(pods.items)}개의 Pod를 찾았습니다.")
            
            # 메트릭 데이터 가져오기 - Custom Resource Definition API 사용
            pod_metrics_dict = {}
            try:
                # 메트릭 API 접근
                api_client = client.ApiClient()
                metrics_api_path = f"/apis/metrics.k8s.io/v1beta1/namespaces/{self.namespace}/pods"
                
                print(f"메트릭 API에 접근 시도: {metrics_api_path}")
                # API 설정 확인
                print(f"API 서버 주소: {api_client.configuration.host}")
                
                # 디버깅을 위한 옵션
                api_client.configuration.debug = False
                
                # API 호출 시도
                try:
                    response = api_client.call_api(
                        metrics_api_path, 'GET',
                        auth_settings=['BearerToken'], 
                        response_type='object',
                        _return_http_data_only=True
                    )
                except Exception as api_error:
                    print(f"메트릭 API 호출 실패: {api_error}")
                    # 대안: 직접 kubectl 호출
                    try:
                        print("kubectl을 통해 메트릭 데이터 가져오기 시도...")
                        import subprocess
                        result = subprocess.run(
                            ['kubectl', 'get', '--raw', f'/apis/metrics.k8s.io/v1beta1/namespaces/{self.namespace}/pods'],
                            capture_output=True, text=True, check=False
                        )
                        if result.returncode == 0:
                            import json
                            response = json.loads(result.stdout)
                            print("kubectl을 통해 메트릭 데이터를 성공적으로 가져왔습니다.")
                        else:
                            print(f"kubectl 오류: {result.stderr}")
                            raise Exception(f"kubectl을 통한 메트릭 접근 실패: {result.stderr}")
                    except Exception as kubectl_error:
                        print(f"kubectl 명령어 실행 실패: {kubectl_error}")
                        raise kubectl_error
                
                if response and 'items' in response:
                    print(f"메트릭 API에서 {len(response['items'])}개의 Pod 메트릭을 가져왔습니다.")
                    for pod_metric in response['items']:
                        pod_name = pod_metric['metadata']['name']
                        containers = {}
                        for container in pod_metric.get('containers', []):
                            container_name = container['name']
                            usage = container.get('usage', {})
                            cpu = usage.get('cpu', '0')
                            memory = usage.get('memory', '0')
                            containers[container_name] = {
                                'cpu': cpu,
                                'memory': memory
                            }
                        pod_metrics_dict[pod_name] = containers
                else:
                    print("메트릭 API에서 데이터를 가져오지 못했습니다.")
            except Exception as e:
                print(f"메트릭 API 접근 중 오류 발생: {e}")
                print("기본 리소스 사용량 값(0)을 사용합니다.")
            
            # 각 Pod에 대한 정보 및 메트릭 수집
            for pod in pods.items:
                pod_name = pod.metadata.name
                node_name = pod.spec.node_name or "unknown"
                
                # Pod 정보 설정
                pod_info_dict = {
                    'name': pod_name,
                    'node': node_name,
                    'status': pod.status.phase,
                    'creation_timestamp': pod.metadata.creation_timestamp.strftime('%Y-%m-%dT%H:%M:%SZ') if pod.metadata.creation_timestamp else ""
                }
                self.pod_info.add_metric([self.namespace, pod_name, node_name], pod_info_dict)
                
                # 컨테이너별 리소스 요청 및 제한 설정
                for container in pod.spec.containers:
                    container_name = container.name
                    
                    # Request 및 Limit 정보 추출
                    cpu_request = 0
                    cpu_limit = 0
                    memory_request = 0
                    memory_limit = 0
                    
                    if container.resources and container.resources.requests:
                        cpu_request = self._parse_cpu_value(container.resources.requests.get('cpu', '0'))
                        memory_request = self._parse_memory_value(container.resources.requests.get('memory', '0'))
                    
                    if container.resources and container.resources.limits:
                        cpu_limit = self._parse_cpu_value(container.resources.limits.get('cpu', '0'))
                        memory_limit = self._parse_memory_value(container.resources.limits.get('memory', '0'))
                    
                    self.pod_cpu_request.add_metric([self.namespace, pod_name, container_name], cpu_request)
                    self.pod_cpu_limit.add_metric([self.namespace, pod_name, container_name], cpu_limit)
                    self.pod_mem_request.add_metric([self.namespace, pod_name, container_name], memory_request)
                    self.pod_mem_limit.add_metric([self.namespace, pod_name, container_name], memory_limit)
                    
                    # CPU/메모리 사용량 - 메트릭 API에서 가져온 데이터 사용
                    cpu_usage = 0
                    memory_usage = 0
                    
                    if pod_name in pod_metrics_dict and container_name in pod_metrics_dict[pod_name]:
                        container_metrics = pod_metrics_dict[pod_name][container_name]
                        cpu_usage = self._parse_cpu_value(container_metrics.get('cpu', '0'))
                        memory_usage = self._parse_memory_value(container_metrics.get('memory', '0'))
                    
                    self.pod_cpu_usage.add_metric([self.namespace, pod_name, container_name], cpu_usage)
                    self.pod_mem_usage.add_metric([self.namespace, pod_name, container_name], memory_usage)
        
        except ApiException as e:
            print(f"Kubernetes API 예외 발생: {e}")
        except Exception as e:
            print(f"예외 발생: {e}")
    
    def _parse_cpu_value(self, cpu_str):
        """CPU 값을 코어 단위로 변환"""
        if not cpu_str:
            return 0
            
        if isinstance(cpu_str, (int, float)):
            return float(cpu_str)
            
        cpu_str = str(cpu_str)
        if cpu_str.endswith('n'):
            return float(cpu_str[:-1]) / 1000000000
        elif cpu_str.endswith('u'):
            return float(cpu_str[:-1]) / 1000000
        elif cpu_str.endswith('m'):
            return float(cpu_str[:-1]) / 1000
        else:
            return float(cpu_str)
    
    def _parse_memory_value(self, memory_str):
        """메모리 값을 바이트 단위로 변환"""
        if not memory_str:
            return 0
            
        if isinstance(memory_str, (int, float)):
            return float(memory_str)
            
        memory_str = str(memory_str)
        if memory_str.endswith('Ki'):
            return float(memory_str[:-2]) * 1024
        elif memory_str.endswith('Mi'):
            return float(memory_str[:-2]) * 1024 * 1024
        elif memory_str.endswith('Gi'):
            return float(memory_str[:-2]) * 1024 * 1024 * 1024
        elif memory_str.endswith('Ti'):
            return float(memory_str[:-2]) * 1024 * 1024 * 1024 * 1024
        elif memory_str.endswith('k'):
            return float(memory_str[:-1]) * 1000
        elif memory_str.endswith('M'):
            return float(memory_str[:-1]) * 1000 * 1000
        elif memory_str.endswith('G'):
            return float(memory_str[:-1]) * 1000 * 1000 * 1000
        elif memory_str.endswith('T'):
            return float(memory_str[:-1]) * 1000 * 1000 * 1000 * 1000
        else:
            return float(memory_str)
    
    def collect(self):
        """Prometheus 콜렉터용 collect 메소드"""
        self.pod_cpu_usage = GaugeMetricFamily(
            'pod_cpu_usage_cores',
            'CPU usage in cores',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_mem_usage = GaugeMetricFamily(
            'pod_memory_usage_bytes',
            'Memory usage in bytes',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_cpu_request = GaugeMetricFamily(
            'pod_cpu_request_cores',
            'CPU request in cores',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_cpu_limit = GaugeMetricFamily(
            'pod_cpu_limit_cores',
            'CPU limit in cores',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_mem_request = GaugeMetricFamily(
            'pod_memory_request_bytes',
            'Memory request in bytes',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_mem_limit = GaugeMetricFamily(
            'pod_memory_limit_bytes',
            'Memory limit in bytes',
            labels=['namespace', 'pod', 'container']
        )
        self.pod_info = InfoMetricFamily(
            'pod_info',
            'Pod information',
            labels=['namespace', 'pod', 'node']
        )
        
        self.collect_pod_metrics()
        
        yield self.pod_cpu_usage
        yield self.pod_mem_usage
        yield self.pod_cpu_request
        yield self.pod_cpu_limit
        yield self.pod_mem_request
        yield self.pod_mem_limit
        yield self.pod_info
    
    def run(self):
        """
        메트릭 수집기 실행
        Prometheus 클라이언트 HTTP 서버 시작
        """
        # 커스텀 콜렉터 등록
        REGISTRY.register(self)
        
        # Prometheus 클라이언트 HTTP 서버 시작
        start_http_server(self.metrics_port)
        print(f"메트릭 서버 시작됨 - 포트 {self.metrics_port}")
        
        try:
            while True:
                time.sleep(10)  # 10초마다 업데이트 (Prometheus가 scrape할 때 최신 데이터 제공)
        except KeyboardInterrupt:
            print("프로그램 종료")

def main():
    """메인 함수"""
    parser = argparse.ArgumentParser(description='KubeMetrics Exporter - Kubernetes 메트릭 수집 및 Prometheus 노출')
    parser.add_argument('--namespace', '-n', default='default', help='모니터링할 네임스페이스')
    parser.add_argument('--port', '-p', type=int, default=8000, help='메트릭 서버 포트')
    
    args = parser.parse_args()
    
    # 메트릭 수집기 실행
    exporter = KubeMetricsExporter(args.namespace, args.port)
    exporter.run()

if __name__ == '__main__':
    main()