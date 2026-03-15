include .env
export

S3 := s3cmd --access_key=$(SCW_ACCESS_KEY) --secret_key=$(SCW_SECRET_KEY) \
	--host=$(S3_ENDPOINT) --host-bucket='%(bucket)s.$(S3_ENDPOINT)' \
	--no-mime-magic --guess-mime-type

ROOT_FILES := index.html catalogue.css catalogue.js catalogue-data.js

.PHONY: deploy build

build:
	bun run build-catalogue.ts

deploy: build
	@for f in $(ROOT_FILES); do $(S3) put --acl-public $$f $(S3_BUCKET)/$$f; done
	@$(S3) sync --acl-public --delete-removed --exclude 'TEMPLATE.md' --exclude '.DS_Store' docs/ $(S3_BUCKET)/docs/
	@$(S3) sync --acl-public --delete-removed --exclude '*.md' --exclude '*.sh' schemas/ $(S3_BUCKET)/schemas/
	@echo "✓ $(S3_PUBLIC_URL)"
