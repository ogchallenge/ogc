# OGC 정적 웹사이트

OGC(Optimization Grand Challenge) 연도별 안내 페이지를 정적 HTML로 서비스합니다.

## 📁 주요 구조

- `index.html`, `styles.css`: 루트 포털 페이지
- `2024/`, `2025/`, `2026/`: 연도별 소스
- `build_dist.py`: 해시 기반 배포 파일 생성 스크립트
- `file_hashing.txt`: 루트 해시 대상 설정
- `2024/file_hashing.txt` (연도별 동일): 연도 해시 대상 설정
- `2024/release.txt` (연도별 동일): GitHub Release 업로드 대상 설정
- `2024/release_versions.json` (연도별 자동 생성): 파일별 버전/해시 기록
- `release_assets/<year>/` (자동 생성): GitHub Release 업로드용 에셋 산출물
- `docs/`: GitHub Pages 배포용 산출물(자동 생성)

## 🚀 로컬에서 실행하기

### 파일명 해시 기반 docs 빌드

```bash
cd webpage
python3 build_dist.py
```

루트 폴더와 각 연도 폴더의 `file_hashing.txt`에 해시 대상을 지정할 수 있습니다.

기본값:

```txt
*.html
*.css
markdown
```

빌드가 완료되면 `docs/` 폴더가 생성되며, 지정된 대상 파일/폴더는 해시가 포함된 파일명으로 생성됩니다.
연도별 `index.html`이 해시 대상인 경우, `docs/<year>/index.html`은 해시된 HTML로 리다이렉트하는 로더로 유지됩니다.
루트 `index.html`이 해시 대상인 경우에도 동일하게 `docs/index.html`은 해시된 HTML로 리다이렉트하는 로더를 유지합니다.

### 간단한 웹서버로 테스트

```bash
cd webpage
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000` 으로 접속하면 됩니다.

### Node.js HTTP 서버 사용

```bash
cd webpage
npx http-server -p 8000
```

## 🌐 GitHub Pages에 배포하기

`main` 브랜치의 `docs/` 폴더를 Source로 사용합니다.

### 설정 및 배포

1. GitHub 저장소에 `webpage` 전체를 push합니다.
2. GitHub 저장소 Settings → Pages에서 다음처럼 설정합니다.
  - Source: `Deploy from a branch`
  - Branch: `main`
  - Folder: `/docs`
3. 로컬에서 배포 산출물을 생성합니다.

```bash
cd webpage
python3 build_dist.py
git add .
git commit -m "Update docs for GitHub Pages"
git push
```

4. 약 1-2분 후 Pages URL에서 사이트를 확인합니다.

## 🔄 콘텐츠 업데이트

연도별 마크다운/스타일/HTML을 수정한 후:

```bash
python3 build_dist.py
```

명령어로 해시 기반 배포 파일(`docs/`)을 자동 재생성할 수 있습니다.

## 📦 GitHub Release 연동

각 연도 폴더(`2024/`, `2025/`, `2026/`)의 `release.txt`에 업로드 대상 파일/폴더를 지정합니다.

예시 (`2024/release.txt`):

```txt
instances/train/stage3_problems.zip
baselines
instances/test/*.zip
```

`python3 build_dist.py` 실행 시:

1. `release.txt` 대상 파일을 수집합니다.
2. 파일 내용(SHA-256)을 기준으로 버전을 관리합니다.
  - 변경 없음: 기존 버전 유지
  - 내용 변경: patch 버전 `0.0.1`씩 증가 (예: `0.0.3` → `0.0.4`)
3. 업로드용 파일을 `release_assets/<year>/`에 생성합니다.
4. 파일별 URL을 GitHub Release 다운로드 URL로 계산하고,
  해당 파일을 가리키는 마크다운 링크를 자동 치환합니다.
5. 상태 파일 `release_versions.json`, 매니페스트 `release_manifest.json`을 갱신합니다.

`release_assets/<year>/upload_release_assets.sh` 스크립트를 사용하면 `gh` CLI로 업로드할 수 있습니다.



## 🎨 기술 스택

- **HTML5**: 시맨틱 HTML
- **CSS3**: 모던 CSS (CSS Grid, Flexbox)
- **Python**: 마크다운 → HTML 변환 (markdown2)
- **GitHub Pages**: 호스팅

## ✨ 특징

- 📱 완전 반응형 디자인 (모바일/태블릿/데스크톱)
- 🎯 깔끔하고 현대적인 UI
- 🗂️ 사이드바 네비게이션으로 쉬운 이동
- 🚀 정적 사이트라 빠른 로딩
- ♿ 접근성을 고려한 설계

## 📝 라이선스

OGC2024 공식 콘텐츠를 기반으로 제작되었습니다.
