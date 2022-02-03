crosssums: build/.image
	docker run \
		-it \
		-v `pwd`:/w \
		-w /w \
		cross-sums:latest $(ARGS)

shell: build/.image
	docker run \
		-it \
		-v `pwd`:/w \
		-w /w \
		--entrypoint bash \
		cross-sums:latest

image_deps = $(shell find python -type f)
build/.image: Dockerfile build/.build $(image_deps)
	docker build \
		--progress=plain \
		-t cross-sums:latest \
		.
	touch build/.image

build/.build:
	mkdir build
	touch build/.build
