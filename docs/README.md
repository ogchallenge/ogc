# OGC 정적 웹사이트

OGC(Optimization Grand Challenge) 연도별 안내 페이지를 정적 HTML로 서비스합니다.

## 📁 주요 구조

- `index.html`, `styles.ec248aaf09.css`: 루트 포털 페이지
- `2024/`, `2025/`, `2026/`: 연도별 소스
- `build_dist.py`: 해시 기반 배포 파일 생성 스크립트
- `file_hashing.txt`: 루트 해시 대상 설정
- `<year>/file_hashing.txt`: 연도별 해시 대상 설정
- `<year>/release.txt`: GitHub Release 업로드 대상 설정
- `<year>/release_versions.json` (자동 생성): 파일별 버전/해시 기록
- `<year>/release_manifest.json` (자동 생성): 릴리즈 매핑/변경 파일 기록
- `release_assets/<year>/` (자동 생성): GitHub Release 업로드용 에셋 산출물
- `docs/`: GitHub Pages 배포용 산출물(자동 생성)

## ⚙️ 핵심 설정 파일 상세

아래 3개 파일이 빌드/배포 동작을 결정합니다.

### 1) `file_hashing.txt`

해시 파일명으로 변환할 대상을 정의합니다. 루트용 1개, 연도별(`2024/`, `2025/`, `2026/`) 1개씩 존재합니다.

- 지원 형식
  - 파일: `index.html`
  - 폴더: `markdown`
  - 와일드카드: `*.html`, `assets/**/*.png`
- 주석(`#`)과 빈 줄은 무시됩니다.
- 기본값(파일이 없을 때 자동 생성):

```txt
*.html
*.css
markdown
```

동작 요약:

- 지정된 파일은 `name.<hash>.ext` 형태로 변경됩니다.
- `index.html`이 해시 대상이면 `docs/index.html`(또는 `docs/<year>/index.html`)은 해시된 실제 파일로 redirect하는 로더로 유지됩니다.

### 2) `release.txt`

GitHub Release로 배포할 원본 파일/폴더를 정의합니다. `build_dist.py`는 이 목록을 기준으로 릴리즈 자산을 생성하고 링크를 치환합니다.

- 지원 형식
  - 파일: `instances/train/stage3_problems.zip`
  - 폴더: `baselines`
  - 와일드카드: `instances/**/*.zip`, `algorithms/*.zip`
- 주석(`#`)과 빈 줄은 무시됩니다.
- `*`는 현재 경로 레벨 기준, 하위 폴더 재귀 포함은 `**` 사용
  - 예: `instances/**/*.zip`

예시(`2024/release.txt`):

```txt
instances/**/*.zip
algorithms/*.zip
```

빌드 시 동작:

1. `release.txt`에 정의된 파일 집합을 수집
2. `docs/` 복사 단계에서 해당 파일/폴더 제외
3. GitHub Release 업로드 대상 자산(`release_assets/<year>/`) 생성
4. 마크다운 내 상대 링크를 release URL로 자동 치환

### 3) `contents.json`

연도별 마크다운 네비게이션 구조를 정의하는 파일입니다. 위치는 `<year>/markdown/contents.json`입니다.

주요 필드:

- `pages`: 실제 문서 목록
  - `id`: 페이지 식별자(해시 라우팅 키)
  - `file`: 마크다운 파일명
  - `title`: `{ "ko": "...", "en": "..." }`
- `sections`: 사이드바 그룹
  - `title`: 섹션 제목(ko/en)
  - `items`: `pages[].id` 배열

간단 예시:

```json
{
  "pages": [
    {
      "id": "main",
      "file": "main.md",
      "title": { "ko": "메인", "en": "Main" }
    }
  ],
  "sections": [
    {
      "title": { "ko": "안내", "en": "Guide" },
      "items": ["main"]
    }
  ]
}
```

빌드 시 `contents.json`도 해시 파일명(`contents.<hash>.json`)으로 변환되며, HTML의 fetch 경로가 자동으로 갱신됩니다.

## 📦 GitHub Release 버전 규칙

릴리즈 대상 파일의 버전은 `<year>/release_versions.json`으로 관리됩니다.

- 최초 감지 파일: `1.0.0`
- 내용 동일(SHA-256 동일): 버전 유지, 업로드 생략
- 내용 변경(SHA-256 변경): patch `+0.0.1` 증가, 변경 파일만 업로드

예:

- `1.0.0` → `1.0.1`
- `1.0.1` → `1.0.2`

`<year>/release_manifest.json`에는 `changed_assets`(이번 빌드에서 실제 업로드 대상)와 전체 자산 매핑이 기록됩니다.

## 🚀 로컬 빌드/실행

### docs 빌드

```bash
cd webpage
python3 build_dist.py
```

### 간단한 웹서버 테스트

```bash
cd webpage
python3 -m http.server 8000
```

브라우저에서 `http://localhost:8000` 접속

### Node.js HTTP 서버

```bash
cd webpage
npx http-server -p 8000
```

## 🌐 GitHub Pages 배포

`main` 브랜치의 `docs/` 폴더를 Source로 사용합니다.

1. 저장소에 `webpage` 전체 push
2. GitHub Settings → Pages
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
3. 로컬에서 배포 산출물 생성 및 push

```bash
cd webpage
python3 build_dist.py
git add .
git commit -m "Update docs for GitHub Pages"
git push
```

## 📝 라이선스

OGC 공식 콘텐츠를 기반으로 제작되었습니다.
