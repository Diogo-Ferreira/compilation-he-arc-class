class CssWriter:
    def __init__(self):
        self.content = ""

    def _write_block(self, selector, block_rules):
        """

        :param block_scope:
        :param block_rules:
        :return:
        """

        return "%s {\n\t%s;\n}\n" % (selector, ";\n\t".join(block_rules))

    def _write_keyframe(self, keyframe_name, keyframe_rules):
        """

        :param keyframe_name:
        :param keyframe_rules:
        :return:
        """

        rules = ["%s {\n\t\t%s;\n\t}" % (perc, rule) for perc, rules in keyframe_rules.iteritems() for rule in rules]

        return "@keyframes %s {\n\t%s\n}\n" % (keyframe_name, "\n\t".join(rules))

    def write_context(self, context):
        for selector, rules in context["selectors"].iteritems():
            self.content += self._write_block(selector, rules)

        for name, rules in context["keyframes"].iteritems():
            self.content += self._write_keyframe(name, rules)

        print(self.content)
