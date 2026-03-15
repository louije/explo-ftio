include .env
export

S3 := s3cmd --access_key=$(SCW_ACCESS_KEY) --secret_key=$(SCW_SECRET_KEY) \
	--host=$(S3_ENDPOINT) --host-bucket='%(bucket)s.$(S3_ENDPOINT)' \
	--no-mime-magic --guess-mime-type

S3_ROOT := $(dir $(S3_BUCKET))

# Only sync these extensions — everything else is ignored
INCLUDE := --include '*.html' --include '*.css' --include '*.js' --include '*.json' --include '*.woff2'
EXCLUDE := --exclude '*'

.PHONY: deploy build

build:
	bun run build-catalogue.ts

deploy: build
	@$(S3) sync --acl-public --delete-removed $(INCLUDE) $(EXCLUDE) ./ $(S3_BUCKET)/
	@$(S3) put --acl-public root-index.html $(S3_ROOT)index.html
	@$(S3) put --acl-public error.html $(S3_ROOT)error.html
	@echo "✓ $(S3_PUBLIC_URL)"
