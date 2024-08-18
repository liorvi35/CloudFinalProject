#!/usr/bin/env python3

import aws_cdk as cdk

from cdk.sn_stack import SnStack


app = cdk.App()
SnStack(app, "SnStack")

app.synth()
