"""
유틸리티 모듈 - 다양한 유틸리티 함수 모음
"""

import json
from typing import Any, Dict, Union

def safe_json_dumps(data: Any) -> str:
    """
    데이터를 안전하게 JSON 문자열로 변환하는 함수
    
    Args:
        data (Any): 변환할 데이터 (문자열, 딕셔너리, 리스트 등)
        
    Returns:
        str: JSON 문자열
        
    Examples:
        >>> safe_json_dumps("hello")
        '{"content": "hello"}'
        >>> safe_json_dumps({"name": "test"})
        '{"name": "test"}'
    """
    try:
        # 문자열인 경우 content 필드로 감싸기
        if isinstance(data, str):
            return json.dumps({"content": data})
        # 이미 딕셔너리나 리스트인 경우 그대로 JSON 변환
        elif isinstance(data, (dict, list)):
            return json.dumps(data)
        # 그 외의 경우 문자열로 변환 후 content 필드로 감싸기
        else:
            return json.dumps({"content": str(data)})
    except Exception as e:
        # 변환 실패 시 기본 JSON 객체 반환
        return json.dumps({"error": f"Invalid data format: {str(e)}", "content": str(data)})

def parse_json_content(json_str: str) -> str:
    """
    JSON 문자열을 파싱하고 다시 문자열로 반환하는 함수
    
    Args:
        json_str (str): 파싱할 JSON 문자열
        
    Returns:
        str: 파싱된 데이터의 문자열 표현
        
    Examples:
        >>> parse_json_content('{"content": "hello"}')
        '{"content": "hello"}'
    """
    try:
        # JSON 파싱 시도
        parsed = json.loads(json_str)
        # 파싱된 데이터가 딕셔너리이고 'content' 키만 있는 경우
        if isinstance(parsed, dict) and len(parsed) == 1 and 'content' in parsed:
            return parsed['content']
        # 그 외의 경우 원본 JSON 문자열 반환
        return json_str
    except json.JSONDecodeError:
        # 파싱 실패 시 원본 문자열 반환
        return json_str 