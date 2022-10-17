import React, { ReactElement, useEffect, useMemo, useState } from "react";
import { Autocomplete, TextField } from "@mui/material";
import { HassEntities, HassEntity } from "home-assistant-js-websocket";
import _ from "lodash";

interface HomeAssistantEntitiesProps {
  entities: HassEntities;
  entity?: string;
  onUpdate: (value: string) => void;
}

interface Option {
  label: string;
  value: string;
}

function HomeAssistantEntities({
  entities,
  entity,
  onUpdate,
}: HomeAssistantEntitiesProps): ReactElement {
  const [value, setValue] = useState<Option | null>(null);

  const options: Array<Option> = useMemo<Array<Option>>(() => {
    return Object.values(entities)
      .filter(
        (entity: HassEntity) => !entity.entity_id.startsWith("device_tracker")
      )
      .sort((a: HassEntity, b: HassEntity) =>
        a.entity_id > b.entity_id ? 1 : a.entity_id < b.entity_id ? -1 : 0
      )
      .map((entity: HassEntity) => ({
        label: entity.attributes.friendly_name
          ? `${entity.attributes.friendly_name} - ${entity.entity_id}`
          : entity.entity_id,
        value: entity.entity_id,
      }));
  }, [entities]);

  function handleChange(
    _event: React.ChangeEvent<unknown>,
    newValue: Option | null
  ): void {
    setValue(newValue);
    if (newValue?.value) onUpdate(newValue.value);
  }

  useEffect(() => {
    if (!value && options && entity) {
      const val = options.find((option: Option) => option.value === entity);
      if (val) setValue(val);
    }
  }, [value, options, entity]);

  return (
    <Autocomplete
      id="entity"
      fullWidth
      options={options}
      groupBy={(option: Option): string =>
        _.upperCase(option.value.split(".")[0])
      }
      getOptionLabel={(option: Option): string => option.label}
      // getOptionSelected={(option: Option): boolean =>
      //   option.value === value?.value
      // }
      value={value || null}
      onChange={handleChange}
      renderInput={(params): ReactElement => (
        <TextField
          {...params}
          placeholder="Search for entities"
          label="Entity"
        />
      )}
    />
  );
}

export default HomeAssistantEntities;
