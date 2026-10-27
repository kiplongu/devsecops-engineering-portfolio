# syntax=docker/dockerfile:1.7
FROM golang:1.27.3-alpine AS build
WORKDIR /src
COPY go.mod ./
COPY cmd ./cmd
COPY internal ./internal
RUN CGO_ENABLED=0 GOOS=linux go test ./... \
    && CGO_ENABLED=0 GOOS=linux go build -trimpath -ldflags="-s -w" -o /out/portfolio-api ./cmd/server

FROM scratch
LABEL org.opencontainers.image.title="DevSecOps portfolio sample API" \
      org.opencontainers.image.description="Minimal non-root service used to exercise the portfolio security controls"
COPY --from=build /out/portfolio-api /portfolio-api
USER 65532:65532
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 CMD ["/portfolio-api", "healthcheck"]
ENTRYPOINT ["/portfolio-api"]
