<?php

namespace App\Http\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class FactVehicleCountResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id' => $this->id,
            'full_date' => $this->date->full_date ?? null, // Assumindo que dim_date tem 'full_date'
            'year' => $this->date->year ?? null,
            'month' => $this->date->month ?? null,
            'day' => $this->date->day ?? null,
            'weekday' => $this->date->weekday ?? null,
            'full_time' => $this->time->full_time ?? null, // Assumindo que dim_time tem 'full_time'
            'hour' => $this->time->hour ?? null,
            'minute' => $this->time->minute ?? null,
            'period' => $this->time->period ?? null,
            'location' => $this->location->location ?? null, // Assumindo que dim_location tem 'location'
            'location_old' => $this->location->location_old ?? null,
            'direction' => $this->location->direction ?? null,
            'direction_old' => $this->location->direction_old ?? null,
            'car' => $this->car,
            'motorcycle' => $this->motorcycle,
            'bike' => $this->bike,
            'truck' => $this->truck,
            'bus' => $this->bus,
            'n' => $this->n,
            's' => $this->s,
            'e' => $this->e,
            'w' => $this->w,
            'ne' => $this->ne,
            'nw' => $this->nw,
            'se' => $this->se,
            'sw' => $this->sw,
        ];
    }
}