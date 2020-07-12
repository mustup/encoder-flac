import logging
import shlex

import mustup.core.format
import mustup.core.tup.rule

logger = logging.getLogger(
    __name__,
)


class Format(
            mustup.core.format.Format,
        ):
    supported_extensions = {
        '.wave',
    }

    supported_transformations = {
        'trim',
    }

    tags_map = {
        'album': 'ALBUM',
        'artist': 'ARTIST',
        'disc number': 'DISCNUMBER',
        'title': 'TITLE',
        'track number': 'TRACKNUMBER',
    }

    def __init__(
                self,
            ):
        pass

    def process(
                self,
                metadata,
                source_basename,
                source_name,
                transformations,
            ):
        output_name = f'{ source_basename }.flac'

        command = [
            'flac',
            '@(FLAC_FLAGS)',
        ]

        try:
            trim_spec = transformations['trim']
        except KeyError:
            pass
        else:
            try:
                time_spec = trim_spec['start']
            except KeyError:
                pass
            else:
                minutes = time_spec.get(
                    'minutes',
                    0,
                )
                seconds = time_spec.get(
                    'seconds',
                    0,
                )
                second_fractions = time_spec.get(
                    'second_fractions',
                    0,
                )
                formatted_time = f'{ minutes }:{ seconds }.{ second_fractions }'

                argument = f'--skip={ formatted_time }'

                command.append(
                    argument,
                )

            try:
                time_spec = trim_spec['duration']
            except KeyError:
                pass
            else:
                minutes = time_spec.get(
                    'minutes',
                    0,
                )
                seconds = time_spec.get(
                    'seconds',
                    0,
                )
                second_fractions = time_spec.get(
                    'second_fractions',
                    0,
                )
                formatted_time = f'{ minutes }:{ seconds }.{ second_fractions }'

                argument = f'--until=+{ formatted_time }'

                command.append(
                    argument,
                )

            try:
                time_spec = trim_spec['end']
            except KeyError:
                pass
            else:
                minutes = time_spec.get(
                    'minutes',
                    0,
                )
                seconds = time_spec.get(
                    'seconds',
                    0,
                )
                second_fractions = time_spec.get(
                    'second_fractions',
                    0,
                )
                formatted_time = f'{ minutes }:{ seconds }.{ second_fractions }'

                argument = f'--until={ formatted_time }'

                command.append(
                    argument,
                )

        try:
            tags = metadata['tags']
        except KeyError:
            pass
        else:
            command.append(
                '--no-utf8-convert',
            )

            # Tags are sorted to ensure consistent ordering of the command line arguments.
            # If ordering varied, tup would run the commands again.

            try:
                common_tags = tags['common']
            except KeyError:
                pass
            else:
                iterator = Format.tags_map.items(
                )

                sorted_pairs = sorted(
                    iterator,
                )

                for pair in sorted_pairs:
                    tag_key = pair[0]
                    vorbis_comment_key = pair[1]
                    try:
                        value = common_tags[tag_key]
                    except KeyError:
                        pass
                    else:
                        multiple_values = isinstance(
                            value,
                            list,
                        )

                        if multiple_values:
                            vorbis_comment_values = value

                            for vorbis_comment_value in vorbis_comment_values:
                                argument = shlex.quote(
                                    f'--tag={ vorbis_comment_key }={ vorbis_comment_value }',
                                )

                                command.append(
                                    argument,
                                )
                        else:
                            vorbis_comment_value = value

                            argument = shlex.quote(
                                f'--tag={ vorbis_comment_key }={ vorbis_comment_value }',
                            )

                            command.append(
                                argument,
                            )

            try:
                vorbis_comments = tags['Vorbis']
            except KeyError:
                pass
            else:
                iterator = vorbis_comments.items(
                )

                sorted_pairs = sorted(
                    iterator,
                )

                for pair in sorted_pairs:
                    vorbis_comment_key = pair[0]
                    value = pair[1]

                    multiple_values = isinstance(
                        value,
                        list,
                    )

                    if multiple_values:
                        vorbis_comment_values = value

                        for vorbis_comment_value in vorbis_comment_values:
                            argument = shlex.quote(
                                f'--tag={ vorbis_comment_key }={ vorbis_comment_value }',
                            )

                            command.append(
                                argument,
                            )
                    else:
                        vorbis_comment_value = value

                        argument = shlex.quote(
                            f'--tag={ vorbis_comment_key }={ vorbis_comment_value }',
                        )

                        command.append(
                            argument,
                        )

        try:
            pictures = metadata['pictures']['APIC']
        except KeyError:
            pass
        else:
            iterator = pictures.items(
            )

            sorted_pairs = sorted(
                iterator,
            )

            for pair in sorted_pairs:
                picture_type = pair[0]
                picture_details = pair[1]
                path = picture_details['path']
                description = picture_details.get(
                    'description',
                    '',
                )

                command.append(
                    '--picture',
                )

                parts = [
                    str(
                        picture_type,
                    ),
                    '',
                    description,
                    '',
                    path,
                ]

                picture_specification = '|'.join(
                    parts,
                )

                argument = shlex.quote(
                    picture_specification,
                )

                command.append(
                    argument,
                )

        command.extend(
            [
                '--output-name',
                shlex.quote(
                    output_name,
                ),
                '--',
                shlex.quote(
                    source_name,
                ),
            ],
        )

        rule = mustup.core.tup.rule.Rule(
            inputs=[
                source_name,
            ],
            command=command,
            outputs=[
                output_name,
            ],
        )

        return rule
