import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { MatTabBody } from '@angular/material/tabs';

@Injectable({
  providedIn: 'root'
})

export class ApiService {
  constructor(private http: HttpClient) { }

  userLoggedIn(): Observable<{}> {
    return this.http.get('/api/user/current', {observe: 'response'});
  }

  /**
   * Get server ten codes
   * 
   * @returns 200
   */
  getTenCodes() {
    return this.http.get('/api/server/tencodes', {observe: 'body', responseType: 'json'});
  }

  /**
   * Get the current user
   * 
   * @returns 200/404/403
   */
  getCurrentUser() {
    return this.http.get('/api/user/current', {observe: 'body', responseType: 'json'});
  }

  getCurrentUserCharacters() {
    return this.http.get('/api/user/current/characters', {observe: 'body', responseType: 'json'});
  }

  /**
   * Get user by Discord ID
   * 
   * @param discordId {string}
   * @returns An `Observable` of the response body as a JSON object.
   */
  getUser(discordId: string) {
    return this.http.get(`/api/user/${discordId}`, {observe: 'body', responseType: 'json'});
  }

  /**
   * Delete User
   * 
   * @param discordId {string}
   * @returns 200
   */
  deleteUser(discordId: string) {
    return this.http.delete(`/api/user/${discordId}`, {observe: 'body', responseType: 'json'});
  }

  /**
   * Add department permission for user
   * 
   * @param discordId {string}
   * @param departmentId {number}
   * @returns 200/404/400/409
   */
  addUserDepartment(discordId: string, departmentId: number) {
    return this.http.put(`/api/user/${discordId}/department/${departmentId}`, {observe: 'body', responseType: 'json'})
  }

  /**
   * Remove department permission for user
   * 
   * @param discordId {string}
   * @param departmentId {number}
   * @returns 200/404/400/409
   */
  removeUserDepartment(discordId: string, departmentId: number) {
    return this.http.delete(`/api/user/${discordId}/department/${departmentId}`, {observe: 'body', responseType: 'json'})
  }

  /**
   * Get all users
   * 
   * @returns 200/403
   */
  getAllUsers() {
    return this.http.get(`/api/user/all`, {observe: 'body', responseType: 'json'});
  }

  /**
   * Get all departments
   * 
   * @returns 200
   */
  getAllDepartments() {
    return this.http.get(`/api/department/all`, {observe: 'body', responseType: 'json'});
  }

  /**
   * Get department by ID
   * 
   * @param departmentId {string}
   * @returns 200
   */
  getDepartment(departmentId: number) {
    return this.http.get(`/api/department/${departmentId}`, {observe: 'body', responseType: 'json'})
  }

  /**
   * Create person/character
   * 
   * @param firstName {string}
   * @param lastName {string}
   * @param address {string}
   * @param dateOfBirth {string}
   * @param sex {string}
   * @param gender {string}
   * @param race {string}
   * @param height {string}
   * @returns 200
   */
  createPerson(
    firstName: string, lastName: string,
    address: string, dateOfBirth: string,
    sex: string, gender: string, race: string,
    height: string
  ) 
  {
    return this.http.put('/api/vehicle/create',
      {params: new HttpParams()
        .set('firstName', firstName)
        .set('lastName', lastName)
        .set('address', address)
        .set('dateOfBirth', dateOfBirth)
        .set('sex', sex)
        .set('gender', gender)
        .set('race', race)
        .set('height', height)
      }
    );
  }

  /**
   * Get a person (character) by their first and last name
   * 
   * @param firstName {string}
   * @param lastName {string}
   * @returns 200/404
   */
  getPerson(firstName: string, lastName: string) {
    return this.http.get('/api/character/search',
      {params: new HttpParams()
        .set('lastName', lastName)
        .set('firstName', firstName),
        observe: 'body', responseType: 'json'
      }
    );
  }

  /**
   * Get person (character) by their characterId 
   * 
   * @param characterId {number}
   * @returns 200/404
   */
  getPersonById(characterId: number) {
    return this.http.get(`/api/character/${characterId}`, {observe: 'body', responseType: 'json'});
  }

  getAllCharacters() {
    return this.http.get('/api/character/all', {observe: 'body', responseType: 'json'});
  }

  /**
   * Create Vehicle
   * 
   * @param licensePlate {string}
   * @param characterId {number}
   * @param stolen {number}
   * @returns 200/403/404
   */
  createVehicle(licensePlate: string, characterId: number, stolen: number) {
    return this.http.put('/api/vehicle/create',
      {params: new HttpParams()
        .set('licensePlate', licensePlate)
        .set('characterId', characterId)
        .set('stolen', stolen)
      }
    );
  }

  /**
   * Get vehicle
   * 
   * @param licensePlate 
   * @returns 200/404
   */
  getVehicle(licensePlate: string) {
    return this.http.get(`/api/vehicle/${licensePlate}`, {observe: 'body', responseType: 'json'});
  }

  /**
   * Register unit -- should be called after submitting portal form
   * 
   * @param departmentId {number}
   * @param unitId {string}
   * @returns 200
   */
  registerUnit(departmentId: number, unitId: string) {
    const params = new HttpParams().set('unitId', unitId).set('departmentId', departmentId);
    return this.http.post('/api/unit/register', null, {params:params});
  }

  /**
   * Get current Unit
   * 
   * @returns 200/404
   */
  getCurrentUnit() {
    return this.http.get('/api/unit/current', {observe: 'body', responseType: 'json'})
  }

  changeUnitStatus(unitId: string, status: number) {
    const params = new HttpParams().set('unitId', unitId);
    return this.http.post(`/api/unit/status/${status}`, {observe: 'body', responseType: 'json'}, {params: params})
  }

  /**
   * Get All Units
   * 
   * @returns 200/403
   */
  getAllUnits() {
    return this.http.get('/api/unit/all', {observe: 'body', responseType: 'json'})
  }

  /**
   * Attatch unit to call
   */
  attachUnit(callId: string, unitId: string) {
    const params = new HttpParams().set('unitId', unitId).set('callId', callId);
    return this.http.post('/api/unit/attach', null, {params:params});
  }

  changeCurrentUnitStatus(statusId: number) {
    return this.http.post(`/api/unit/current/status/${statusId}`, {observe: 'body', responseType: 'json'})
  }

  getCallTypes() {
    return this.http.get('/api/call/types', {observe: 'body', responseType: 'json'})
  }

  getAllCalls() {
    return this.http.get('/api/call/all', {observe: 'body', responseType: 'json'})
  }

  createCall(type: number, subTypeCode: string, postal: number, location: string, description: string) {
    return this.http.put('/api/call/create', null,
      {params: new HttpParams()
        .set('type', type)
        .set('subTypeCode', subTypeCode)
        .set('postal', postal)
        .set('location', location)
        .set('description', description),
        observe: 'body', responseType: 'json'
      }
    );
  }

  deleteCall(callId: string) { return this.http.delete(`/api/call/delete/${callId}`); }


  
}
