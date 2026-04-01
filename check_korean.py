#!/usr/bin/env python3
"""
한글 깨짐 검사 스크립트
문서에서 비정상적인 문자(한글, 영문, 숫자, 기본 특수문자 제외)를 찾아줍니다.
"""

import os
import sys
import re

def check_file(filepath):
    """파일에서 비정상적인 문자를 찾습니다."""
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return [{'line': 0, 'char': '', 'issue': f'파일 읽기 오류: {e}'}]
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines, 1):
        for j, c in enumerate(line, 1):
            o = ord(c)
            # 비정상적인 문자 체크
            if o > 127:
                # 한글 자모음 범위 제외
                if not ('가' <= c <= '힣' or 'ㄱ' <= c <= 'ㅎ' or 'ㅏ' <= c <= 'ㅣ'):
                    # 허용되는 특수문자 제외
                    allowed = ' \t|()-/_.,:!?<>\'"~`[]{}#*+=%/\\$@'
                    if c not in allowed:
                        issues.append({
                            'line': i,
                            'char': c,
                            'code': f'U+{o:04X}',
                            'context': line[:60] + '...' if len(line) > 60 else line
                        })
    
    return issues

def check_directory(directory, extensions=['.md', '.txt']):
    """디렉토리 내 모든 문서를 검사합니다."""
    results = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                issues = check_file(filepath)
                if issues:
                    results[filepath] = issues
    
    return results

def main():
    # 현재 디렉토리 또는 지정된 경로
    target = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    print(f"=== 한글 깨짐 검사: {target} ===\n")
    
    if os.path.isfile(target):
        issues = check_file(target)
        if issues:
            print(f"❌ {target}: {len(issues)}개의 문제 발견\n")
            for issue in issues:
                print(f"  줄 {issue['line']}: '{issue['char']}' ({issue['code']})")
                print(f"    {issue['context']}")
        else:
            print(f"✅ {target}: 문제 없음")
    
    elif os.path.isdir(target):
        results = check_directory(target)
        
        if not results:
            print("✅ 모든 문서가 정상입니다.")
            return 0
        
        print(f"❌ {len(results)}개 파일에서 문제 발견\n")
        
        for filepath, issues in results.items():
            rel_path = os.path.relpath(filepath, target)
            print(f"=== {rel_path} ({len(issues)}개 문제) ===")
            for issue in issues[:5]:  # 파일당 최대 5개만 표시
                print(f"  줄 {issue['line']}: '{issue['char']}' ({issue['code']})")
            if len(issues) > 5:
                print(f"  ... 외 {len(issues) - 5}개")
            print()
        
        return 1
    
    else:
        print(f"오류: {target}은(는) 파일 또는 디렉토리가 아닙니다.")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
