# OGC2024 정적 웹사이트

Notion의 OGC2024 공식 안내를 정적 HTML 웹사이트로 변환했습니다.

## 📁 폴더 구조

```
webpage/
├── index.96880a0834.html              # 홈페이지
├── styles.1891b01169.css              # 메인 스타일시트
├── pages/                  # 각 섹션별 HTML 페이지
│   ├── problem-description.html
│   ├── baseline-algorithm.html
│   ├── preliminary-practice.html
│   ├── preliminary-results.html
│   ├── main-practice.html
│   ├── main-results.html
│   ├── final-practice.html
│   ├── final-submission.html
│   ├── final-results-algorithms.html
│   └── final-results.html
├── assets/                 # 이미지 및 미디어 파일
├── ogc2024/                # Notion 내용 백업
├── generate_pages.py       # 마크다운 → HTML 변환 스크립트
├── update_links.py         # 링크 업데이트 스크립트
└── rename_files.py         # 파일명 변경 스크립트
```

## 🚀 로컬에서 실행하기

### 파일명 해시 기반 dist 빌드

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

빌드가 완료되면 `dist/` 폴더가 생성되며, 지정된 대상 파일/폴더는 해시가 포함된 파일명으로 생성됩니다.
연도별 `index.96880a0834.html`이 해시 대상인 경우, `dist/<year>/index.html`은 해시된 HTML로 리다이렉트하는 로더로 유지됩니다.
루트 `index.96880a0834.html`이 해시 대상인 경우에도 동일하게 `dist/index.html`은 해시된 HTML로 리다이렉트하는 로더를 유지합니다.

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

해시 기반 캐싱 전략을 사용할 때는 `dist/` 폴더를 그대로 배포합니다.

### 방법 1: 간단한 배포

1. GitHub에 새 레포지토리 생성: `ogc2024-website`
2. 로컬에서:

```bash
cd webpage
git init
git add .
git commit -m "Initial commit: OGC2024 static website"
git remote add origin https://github.com/YOUR_USERNAME/ogc2024-website.git
git branch -M main
git push -u origin main
```

3. GitHub 저장소 Settings → Pages → Source를 `main` branch로 설정
4. 약 1-2분 후 `https://YOUR_USERNAME.github.io/ogc2024-website/` 에서 확인

### 방법 2: User/Organization Pages

레포지토리 이름을 `USERNAME.github.io` (또는 `ORGANIZATION.github.io`)로 하면, 
`https://USERNAME.github.io/` 에서 직접 접속할 수 있습니다.

## 🔄 콘텐츠 업데이트

Notion의 마크다운 파일을 `ogc2024/` 폴더에 저장한 후:

```bash
python3 generate_pages.py
```

명령어로 HTML 페이지를 자동으로 재생성할 수 있습니다.

## 📋 포함된 섹션

- **문제 및 알고리즘 제출 안내**
  - 문제설명 및 순위 결정 방법
  - 알고리즘 개발 환경 및 baseline 알고리즘 설명

- **예선**
  - 예선 연습용 문제 및 평가 안내
  - 예선 결과

- **본선**
  - 본선 연습용 문제 및 평가 안내
  - 본선 결과

- **결선**
  - 결선 연습용 문제 및 평가 안내
  - 소스코드 제출, 결선 발표 평가, 시상식 안내
  - 결선 결과 및 알고리즘 공개
  - 최종 결과

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

## 🔗 참고

- [원본 Notion](https://optichallenge.notion.site/OGC2024-be66791b61804bf29e991f6ab6941d5d)
- [GitHub Pages 문서](https://docs.github.com/pages)
