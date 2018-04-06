from shapeworld.dataset import ClassificationDataset
from shapeworld.generators import RandomAttributesGenerator


class ShapeDataset(ClassificationDataset):

    def __init__(
        self,
        world_size=64,
        world_color='black',
        shapes=('square', 'rectangle', 'triangle', 'pentagon', 'cross', 'circle', 'semicircle', 'ellipse'),
        colors=('red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'gray'),
        textures=('solid',),
        rotation=True,
        size_range=(0.1, 0.25),
        distortion_range=(2.0, 3.0),
        shade_range=0.4,
        collision_tolerance=0.25,
        collision_shade_difference=0.5,
        boundary_tolerance=None,
        entity_counts=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15),
        train_entity_counts=(1, 2, 4, 6, 7, 9, 11, 12, 14),
        validation_entity_counts=(3, 8, 13),
        validation_count_rate=0.5,
        test_entity_counts=(5, 10, 15),
        test_count_rate=0.5,
        max_provoke_collision_rate=0.33,
        multi_class=True,
        count_class=False,
        pixel_noise_stddev=0.0
    ):

        if not multi_class and entity_counts == (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15) and train_entity_counts == (1, 2, 4, 6, 7, 9, 11, 12, 14) and validation_entity_counts == (3, 8, 13) and test_entity_counts == (5, 10, 15):
            # correct entity_counts for not multi_class in default setting
            entity_counts = (1,)
            train_entity_counts = (1,)
            validation_entity_counts = (1,)
            test_entity_counts = (1,)

        world_generator = RandomAttributesGenerator(
            world_size=world_size,
            world_color=world_color,
            shapes=shapes,
            colors=colors,
            textures=textures,
            rotation=rotation,
            size_range=size_range,
            distortion_range=distortion_range,
            shade_range=shade_range,
            collision_tolerance=collision_tolerance,
            collision_shade_difference=collision_shade_difference,
            boundary_tolerance=boundary_tolerance,
            entity_counts=entity_counts,
            train_entity_counts=train_entity_counts,
            validation_entity_counts=validation_entity_counts,
            validation_count_rate=validation_count_rate,
            test_entity_counts=test_entity_counts,
            test_count_rate=test_count_rate,
            max_provoke_collision_rate=max_provoke_collision_rate
        )

        assert multi_class == (len(entity_counts) > 1 or entity_counts[0] != 1)
        num_classes = len(world_generator.shapes) * len(world_generator.colors) * len(world_generator.textures)

        super(ShapeDataset, self).__init__(
            world_generator=world_generator,
            num_classes=num_classes,
            multi_class=multi_class,
            count_class=count_class,
            pixel_noise_stddev=pixel_noise_stddev
        )

    def get_classes(self, world):
        if self.count_class:
            return [self.world_generator.shapes.index(entity.shape.name) * len(self.world_generator.colors) * len(self.world_generator.textures) + self.world_generator.colors.index(entity.color.name) * len(self.world_generator.textures) + self.world_generator.textures.index(entity.texture.name) for entity in world.entities]
        elif self.multi_class:
            return {self.world_generator.shapes.index(entity.shape.name) * len(self.world_generator.colors) * len(self.world_generator.textures) + self.world_generator.colors.index(entity.color.name) * len(self.world_generator.textures) + self.world_generator.textures.index(entity.texture.name) for entity in world.entities}
        else:
            return (self.world_generator.shapes.index(world.entities[0].shape.name) * len(self.world_generator.colors) * len(self.world_generator.textures) + self.world_generator.colors.index(world.entities[0].color.name) * len(self.world_generator.textures) + self.world_generator.textures.index(world.entities[0].texture.name),)
