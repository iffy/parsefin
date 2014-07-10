# Copyright (c) Matt Haggard.
# See LICENSE for details.

from twisted.trial.unittest import TestCase, SkipTest
from twisted.internet import utils, defer
from twisted.python.filepath import FilePath
from twisted.python.procutils import which
from twisted.python import log



class ScriptTest(TestCase):


    @defer.inlineCallbacks
    def runScript(self, script):
        """
        Make sure the script runs.
        """
        data = FilePath(__file__).parent().child('data')
        sample_file = data.child('1.input.ofx')

        args = (script, [sample_file.path])
        log.msg('executing %r' % (args,))
        out, err, rc = yield utils.getProcessOutputAndValue(*args, env=None)
        log.msg('rc: %r' % (rc,))
        log.msg('out: %r' % (out,))
        log.msg('err: %r' % (err,))
        if rc != 0:
            self.fail("Failed: %s\n\n%s" % (out, err))


    def test_installed(self):
        """
        The installed script works.
        """
        script = which('parsefin')
        if not script:
            raise SkipTest("Not installed")
        script = script[0]

        return self.runScript(script)


    def test_works(self):
        """
        You can run the parsefin script and it doesn't die.
        """
        script = FilePath(__file__).parent().parent().parent() \
            .child('scripts').child('parsefin').path

        return self.runScript(script)
