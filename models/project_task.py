# -*- coding: utf-8 -*-

##############################################################################
#    Copyright (c) 2021 CODOOS SRL. (http://codoos.com)
#    Maintainer: Eng.Ramadan Khalil (<rkhalil1990@gmail.com>)
#    It is forbidden to publish, distribute, sublicense, or sell copies
#    of the Software or modified copies of the Software.
##############################################################################

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, date


class ProjectTask(models.Model):
    _inherit = 'project.task'

    def write(self, vals):
        old_user_map = {task.id: task.user_ids.mapped('partner_id') for task in self}

        res = super().write(vals)

        if 'user_ids' in vals:
            for task in self:
                old_assignees = old_user_map.get(task.id, self.env['res.partner'])
                new_assignees = task.user_ids.mapped('partner_id')

                followers = task.message_partner_ids

                to_add = new_assignees - followers
                if to_add:
                    task.message_subscribe(partner_ids=to_add.ids)

                removed = old_assignees - new_assignees
                if removed:
                    to_remove = task.message_follower_ids.filtered(
                        lambda f: f.partner_id in removed
                    )
                    if to_remove:
                        to_remove.sudo().unlink()

        return res
