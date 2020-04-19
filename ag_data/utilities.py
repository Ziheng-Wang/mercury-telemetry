import attr

from django.utils import timezone

from ag_data import models
from ag_data.presets.built_in_content import built_in_sensor_types


@attr.s
class MeasurementExchange(object):
    event = attr.ib(kw_only=True, validator=attr.validators.instance_of(models.AGEvent))
    timestamp = attr.ib(
        kw_only=True, validator=attr.validators.instance_of(timezone.datetime)
    )
    sensor = attr.ib(
        kw_only=True, validator=attr.validators.instance_of(models.AGSensor)
    )
    reading = attr.ib(kw_only=True, validator=attr.validators.instance_of(dict))

    @property
    def sensor_type(self):
        return self.sensor.type_id

    @property
    def processing_formula(self):
        return self.sensor_type.processing_formula


def createOrResetAllBuiltInSensorTypes():
    for index in range(len(built_in_sensor_types)):
        sensorType = createOrResetBuiltInSensorTypeAtPresetIndex(index)
        assertSensorType(sensorType)


def createOrResetBuiltInSensorTypeAtPresetIndex(index):
    """Create a sensor type object from available presets of sensor types

        The sensor type record is a prerequisite for any sensor whose type is set to this.
        The sensor type ID is also hardcoded in the database. Therefore, for the same sensor
        type, if this method is called when the record exists, it will update the record.

        Arguments:

            index {int} -- the index of the sensor type preset to use.

        Raises:

            Exception: an exception raises when the index is not valid in presets.
        """

    if index > len(built_in_sensor_types) - 1:
        raise Exception(
            f"Cannot find requested sensor type (index {index}) from presets"
        )
    else:
        pass

    preset = built_in_sensor_types[index]

    # If the sensor type record does not exist in the table, create the record.
    record = models.AGSensorType.objects.filter(id=preset["agSensorTypeID"])

    sensorType = None

    if record.count() == 0:
        sensorType = models.AGSensorType.objects.create(
            id=preset["agSensorTypeID"],
            name=preset["agSensorTypeName"],
            processing_formula=preset["agSensorTypeFormula"],
            format=preset["agSensorTypeFormat"],
        )
    else:
        record = record.first()
        record.name = preset["agSensorTypeName"]
        record.processing_formula = preset["agSensorTypeFormula"]
        record.format = preset["agSensorTypeFormat"]
        record.save()
        sensorType = record

    return sensorType


def createCustomSensorType(name, processing_formula, format):
    sensorType = models.AGSensorType.objects.create(
        id=getNextAvailableSensorTypeID(),
        name=name,
        processing_formula=processing_formula,
        format=format,
    )

    return sensorType


def assertVenue(venue):
    assert isinstance(venue, models.AGVenue), "Missing an instance of AGVenue."


def assertEvent(event):
    assert isinstance(event, models.AGEvent), "Missing an instance of AGEvent."


def assertSensorType(sensorType):
    assert isinstance(
        sensorType, models.AGSensorType
    ), "Not an instance of AGSensorType."


def assertSensor(sensor):
    assert isinstance(sensor, models.AGSensor), "Missing an instance of AGSensor."


def getNextAvailableSensorTypeID():
    maxID = 0
    if models.AGSensorType.objects.count() > 0:
        maxID = models.AGSensorType.objects.latest("id").id

    if maxID % 2 == 0:
        maxID = maxID + 1
    else:
        maxID = maxID + 2

    return maxID