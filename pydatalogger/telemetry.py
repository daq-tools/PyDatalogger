# -*- coding: utf-8 -*-
# (c) 2018 The Hiveeyes Developers <hello@hiveeyes.org>
# License: GNU Affero General Public License, Version 3
import logging

from munch import Munch
from pydatalogger.target import resolve_target_handler

log = logging.getLogger(__name__)


class TelemetryEngine:

    def __init__(self, targets, dry_run):
        self.targets = targets
        self.dry_run = dry_run

    def process(self, data):

        # Configure target subsystems.
        targets = []
        for target_expression in self.targets:
            log.info('Configuring target {}'.format(target_expression))
            target = resolve_target_handler(target_expression, dry_run=self.dry_run)

            if target is None:
                log.error('Could not resolve target {}'.format(target_expression))
                continue

            targets.append(target)

        # Aggregate readings into single message.
        message = Munch()
        item_count = 0
        for reading in data:
            print(reading)
            message[reading.type] = reading.value
            item_count += 1
        log.info('Acquired {} readings'.format(item_count))

        # Emit to active target subsystems.
        for target in targets:
            target.emit(message)

        # Signal readyness to each target subsystem.
        for target in targets:
            target.flush()
