package cmd_test

import (
	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
	. "github.com/onsi/gomega/gbytes"

	"github.com/petewall/eink-radiator/v2/cmd"
)

var _ = Describe("Version", func() {
	var output *Buffer

	BeforeEach(func() {
		output = NewBuffer()
		cmd.VersionCmd.SetOut(output)
	})

	It("prints the version number", func() {
		cmd.Version = "1.2.3"
		cmd.VersionCmd.Run(cmd.VersionCmd, []string{})
		Expect(output).Should(Say("eink-radiator version: 1.2.3"))
	})
})
