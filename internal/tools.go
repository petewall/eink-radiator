// +build tools

package internal

// These tools required by counterfeiter and ginkgo
import (
	_ "github.com/go-task/slim-sprig"
	_ "github.com/google/pprof/profile"
	_ "github.com/maxbrunsfeld/counterfeiter/v6"
	_ "golang.org/x/tools/go/ast/inspector"
)
